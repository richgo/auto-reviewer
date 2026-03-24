# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

`auto-reviewer` is an adversarial, multi-model code review system distributed as an APM package. Multiple LLMs independently review code using atomic **skills**, then cross-examine each other's findings through a debate protocol (detector → challenger → defender → judge). Skills are self-tuning via autoresearch loops scored with SWE-bench-style benchmarks.

## Commands

### Install dependencies
```bash
pip install -r scripts/requirements.txt
gh auth login  # Required: Copilot SDK uses GitHub CLI auth for model selection
```

### Run all tests
```bash
pytest scripts/tests/
```

### Run a specific test file
```bash
pytest scripts/tests/benchmark/test_runner.py
pytest scripts/tests/tune/test_autoresearch_loop.py
```

### Tune a skill (autoresearch loop)
```bash
python scripts/tune/autoresearch.py \
  --skill skills/<skill-id>/SKILL.md \
  --evals evals/<skill-id>.json \
  --model gpt-4o-mini \
  --max-iterations 30 \
  --target-pass-rate 0.95
```

### Run benchmark across models
```bash
python scripts/benchmark/runner.py \
  --skills-dir skills/ \
  --evals-dir evals/ \
  --models gpt-4o-mini,gemini-2.0-flash \
  --output benchmark-results/

python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json \
  --output benchmark-results/REPORT.md
```

### Benchmark a single skill
```bash
SKILL=security-injection
MODELS=gpt-4o-mini,gemini-2.0-flash
RUN_DIR=".tmp-benchmark-${SKILL}"

mkdir -p "$RUN_DIR/skills/${SKILL}" "$RUN_DIR/evals" "$RUN_DIR/output"
cp "skills/${SKILL}/SKILL.md" "$RUN_DIR/skills/${SKILL}/SKILL.md"
cp "evals/${SKILL}.json" "$RUN_DIR/evals/${SKILL}.json"

python scripts/benchmark/runner.py \
  --skills-dir "$RUN_DIR/skills" \
  --evals-dir "$RUN_DIR/evals" \
  --models "$MODELS" \
  --output "$RUN_DIR/output"
```

## Architecture

### The Two Layers

**1. Skill Corpus (`skills/`)**
Each skill is one folder with a single `SKILL.md`. Skills are atomic, testable bug detection units. The naming convention is `<category>-<subcategory>` (e.g., `security-sql-injection`, `concurrency-race-condition`). Skills contain: YAML frontmatter (name, description), detection heuristics, eval cases with buggy code + expected findings, counter-examples for safe code, and binary eval assertions.

**2. Eval Corpus (`evals/`)**
JSON files keyed by skill ID (e.g., `evals/security-injection.json`). Each file has 5–8 cases mixing true positives (buggy code) and counter-examples. Assertions per case: `detected_bug`, `no_false_positive`, `actionable_fix`, `correct_severity`, `evidence_cited`.

### Scripts Architecture (`scripts/`)

- **`tune/`** — Autoresearch loop: `llm_client.py` (Copilot SDK wrapper), `scorer.py` (binary assertion evaluator), `mutator.py` (skill mutation strategies), `autoresearch.py` (CLI entry), `orchestrator.py` (matrix planning for CI)
- **`benchmark/`** — SWE-bench harness: `runner.py` (multi-model evaluation), `reporter.py` (markdown report), `copilot_client.py` (SDK wrapper), `judge.py` (assertion judgment), `scorer.py`
- **`compose/`** — Composer pipeline: `detector.py` (repo signal detection), `selector.py` (policy-mapped skill selection), `composer.py`, `merge.py`, `validator.py`, `versioning.py`; policy config at `scripts/compose/policy.yaml`
- **`skills/`** — Skill utilities: `canonical_inventory.py` (enumerate canonical skill identifiers)

### Agents (`agents/`)

- **`adversarial/agent.md`** — Debate protocol: detector→challenger→defender→judge. Stores state in SQLite at `.auto-reviewer/adversarial.db` (tables: `runs`, `findings`, `stances`, `verdicts`, `cleanup_events`). Resume key: `(repo, pr, commit_sha)`.
- **`composer/agent.md`** — Generates/updates `apm.yml` using repo signals + policy. Commands: `compose` and `compose-update`. Only modifies composer-managed `richgo/auto-reviewer/skills/*` dependencies; preserves all other `apm.yml` sections.

### OpenSpec Agents (`.github/agents/`)

Workflow agents used for spec-driven development of the repo itself:
- `new` → scaffold a change directory under `openspec/changes/<change-name>/`
- `proposal` → write a change proposal
- `design` → architectural design doc
- `specs` → Given/When/Then spec files
- `tasks` → task checklist
- `apply` → implement via BDD+TDD (failing BDD scenario → edge case analysis → TDD red-green-refactor → commit). Commit prefixes: `green: <task>` (unit level), `scenario: <task>` (BDD level)
- `verify` → verify implementation matches specs
- `archive` → merge specs into library

### CI/CD Workflows (`.github/workflows/`)

- **`autoresearch-tuning.yml`** — Runs nightly (or on push to `skills/`/`evals/`) for overnight mutation loops. Generates a matrix of `(skill, model)` pairs, tunes each, then calls `autoresearch-promote.yml` to open promotion PRs.
- **`autoresearch-promote.yml`** — Opens a PR per `autoresearch/<skill>/<model>/<run_id>` branch. Has a `revert_on_regression` job.
- **`benchmark.yml`** — Weekly benchmark on `gpt-4o-mini` and `gemini-2.0-flash`.

## Key Conventions

- **Skill identity is canonical**: one folder per skill, one `SKILL.md`. Skills are the sole source of truth — create `skills/<id>/SKILL.md` directly.
- **Eval assertions are binary**: each assertion (`detected_bug`, `no_false_positive`, etc.) is true/false — the scorer uses an LLM judge to evaluate.
- **Tuning target**: 85–95% pass rate (higher risks overfitting).
- **Autoresearch promotion**: tuned skills are promoted via PR (`autoresearch/<skill>/<model>/<run_id>` branch), not committed directly to `main`.
- **`apm.yml`**: the package manifest. `dependencies.apm` lists skill refs. Composer-managed deps use stable tag pins (`#v1.0.0`) by default.
