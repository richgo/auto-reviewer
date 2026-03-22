import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


def _discover_concern_skill_names(*, concerns_dir: Path) -> List[str]:
    names: List[str] = []
    for path in sorted(concerns_dir.glob("*/SKILL.md")):
        names.append(path.parent.name)
    for path in sorted(concerns_dir.glob("*.md")):
        names.append(path.stem)
    return names


def build_plan(
    *,
    skills_dir: Path,
    evals_dir: Path,
    config_path: Path,
    skills_filter: Optional[List[str]],
    models_filter: Optional[List[str]],
    skills_prefix: Optional[str] = None,
) -> List[Tuple[str, str]]:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    configured_models = [str(model) for model in raw.get("models", [])]
    models = sorted(models_filter or configured_models)

    skill_names = []
    concerns_dir = skills_dir / "concerns"
    for skill_name in _discover_concern_skill_names(concerns_dir=concerns_dir):
        eval_path = evals_dir / f"{skill_name}.json"
        if not eval_path.exists():
            continue
        eval_payload = json.loads(eval_path.read_text(encoding="utf-8"))
        if "review_task" in eval_payload:
            raise ValueError(
                f"Eval payload '{eval_path}' includes review_task, but only skill-linked evals are allowed."
            )
        if skills_filter and skill_name not in skills_filter:
            continue
        if skills_prefix and not skill_name.startswith(skills_prefix):
            continue
        skill_names.append(skill_name)

    return [(skill_name, model) for skill_name in skill_names for model in models]


def build_run_plan(
    *,
    pairs: List[Tuple[str, str]],
    skills_filter: Optional[List[str]],
    models_filter: Optional[List[str]],
    trigger: str,
    run_id: str,
) -> List[Dict[str, str]]:
    filtered = []
    for skill_name, model in pairs:
        if skills_filter and skill_name not in skills_filter:
            continue
        if models_filter and model not in models_filter:
            continue
        filtered.append(
            {
                "run_id": run_id,
                "trigger": trigger,
                "skill": skill_name,
                "model": model,
            }
        )
    return filtered


def compose_run_plan(
    *,
    skills_dir: Path,
    evals_dir: Path,
    config_path: Path,
    skills_filter: Optional[List[str]],
    models_filter: Optional[List[str]],
    skills_prefix: Optional[str] = None,
    trigger: str,
    run_id: str,
) -> List[Dict[str, str]]:
    plan = build_plan(
        skills_dir=skills_dir,
        evals_dir=evals_dir,
        config_path=config_path,
        skills_filter=skills_filter,
        models_filter=models_filter,
        skills_prefix=skills_prefix,
    )
    return build_run_plan(
        pairs=plan,
        skills_filter=skills_filter,
        models_filter=models_filter,
        trigger=trigger,
        run_id=run_id,
    )


def update_model_scores_snapshot(
    *,
    scores_path: Path,
    model: str,
    skill: str,
    metrics: Dict[str, Any],
    accepted: bool,
) -> bool:
    if not accepted:
        return False

    payload = yaml.safe_load(scores_path.read_text(encoding="utf-8")) or {}
    payload.setdefault("models", {})
    payload["models"].setdefault(model, {})
    payload["models"][model][skill] = {
        "pass_rate": float(metrics.get("pass_rate", 0.0)),
        "f1": float(metrics.get("f1", 0.0)),
        "last_run": metrics.get("last_run"),
    }
    payload["last_updated"] = metrics.get("last_run")
    scores_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return True


def build_trajectory_summary(*, history_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    runs = len(history_rows)
    accepted = sum(1 for row in history_rows if bool(row.get("accepted")))
    accept_rate = (accepted / runs) if runs else 0.0
    return {
        "runs": runs,
        "accepted": accepted,
        "accept_rate": accept_rate,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Plan skill × model autoresearch runs")
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--evals-dir", type=Path, default=Path("evals"))
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    parser.add_argument("--skills", help="Comma separated skill names")
    parser.add_argument("--models", help="Comma separated model ids")
    parser.add_argument("--skills-prefix", help="Filter skills by name prefix (e.g. security-)")
    parser.add_argument(
        "--output-format",
        choices=["csv", "github-matrix"],
        default="csv",
        help="Output format: csv (default) or github-matrix (JSON for GitHub Actions matrix)",
    )
    parser.add_argument("--trigger", default="manual")
    parser.add_argument("--run-id")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    skills_filter = [token.strip() for token in args.skills.split(",")] if args.skills else None
    models_filter = [token.strip() for token in args.models.split(",")] if args.models else None
    run_plan = compose_run_plan(
        skills_dir=args.skills_dir,
        evals_dir=args.evals_dir,
        config_path=args.config,
        skills_filter=skills_filter,
        models_filter=models_filter,
        skills_prefix=args.skills_prefix,
        trigger=args.trigger,
        run_id=args.run_id or "manual",
    )
    if args.output_format == "github-matrix":
        matrix_includes = [{"skill": row["skill"], "model": row["model"]} for row in run_plan]
        print(json.dumps({"include": matrix_includes}))
    else:
        for row in run_plan:
            print(f"{row['run_id']},{row['trigger']},{row['skill']},{row['model']}")


if __name__ == "__main__":
    main()
