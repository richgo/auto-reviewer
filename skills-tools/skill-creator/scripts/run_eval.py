#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Uses GitHub Copilot SDK model calls to score whether a skill description
should trigger for each query in an eval set. Outputs results as JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from scripts.copilot_sdk import CopilotSDKClient
    from scripts.utils import parse_skill_md
except ImportError:
    from copilot_sdk import CopilotSDKClient
    from utils import parse_skill_md


TRIGGER_SYSTEM_PROMPT = (
    "You are a strict binary classifier for skill triggering. "
    "Return JSON only."
)


def find_project_root() -> Path:
    """Find repository root by walking up from cwd and looking for .git."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return current


def _build_trigger_prompt(query: str, skill_name: str, skill_description: str) -> str:
    return f"""You are evaluating skill triggering behavior in a Copilot SDK runtime.

Return exactly one JSON object with this schema:
{{
  "triggered": true or false,
  "reason": "short explanation"
}}

Skill name: {skill_name}
Skill description:
{skill_description}

User query:
{query}

Set "triggered" to true only if this query likely needs this skill based on the description.
Do not include markdown, code fences, or extra keys.
"""


def _extract_first_json_object(text: str) -> dict | None:
    decoder = json.JSONDecoder()
    for idx, char in enumerate(text):
        if char != "{":
            continue
        try:
            payload, _ = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def _normalize_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y", "1"}:
            return True
        if lowered in {"false", "no", "n", "0"}:
            return False
    return None


def _parse_triggered(response_text: str) -> bool:
    payload = _extract_first_json_object(response_text)
    if payload is not None:
        parsed = _normalize_bool(payload.get("triggered"))
        if parsed is not None:
            return parsed

    lowered = response_text.strip().lower()
    if re.search(r'"triggered"\s*:\s*true', lowered):
        return True
    if re.search(r'"triggered"\s*:\s*false', lowered):
        return False
    if "true" in lowered and "false" not in lowered:
        return True
    if "false" in lowered and "true" not in lowered:
        return False

    raise ValueError(f"Unable to parse trigger response: {response_text[:200]}")


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run one trigger-eval query using Copilot SDK and return triggered bool."""
    del project_root  # kept for interface compatibility with existing callers
    client = CopilotSDKClient(timeout=timeout)
    response = client.complete(
        prompt=_build_trigger_prompt(query, skill_name, skill_description),
        model=model,
        system=TRIGGER_SYSTEM_PROMPT,
    )
    return _parse_triggered(response)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return aggregate triggering results."""
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            query_triggers.setdefault(query, [])
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        did_pass = (
            trigger_rate >= trigger_threshold
            if should_trigger
            else trigger_rate < trigger_threshold
        )
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Copilot SDK model ID (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, _ = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
