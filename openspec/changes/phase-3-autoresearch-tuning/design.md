# Design: Phase 3 Autoresearch Tuning

## Overview

Phase 3 adds an automated tuning control plane around the existing benchmark and mutation modules so each skill × model pair can improve continuously without manual prompt editing. The design keeps tuning offline, gates promotions on measurable quality deltas, and records a reproducible trajectory of every accepted/rejected mutation. Scheduling and execution are handled by GitHub agentic workflows (weekly + event-driven) that run the loop and open reviewable PRs instead of writing directly to `main`.

## Architecture

### Components Affected
- `scripts/tune/autoresearch.py` — extended from single-loop tuning to deterministic, bounded optimization rounds with convergence checks and promotion metadata.
- `scripts/tune/mutator.py` — constrained mutation generation using failure clusters so candidates remain explainable and diff-bounded.
- `scripts/benchmark/runner.py` — used as the authoritative baseline/re-evaluation engine for candidate gating.
- `scripts/benchmark/scorer.py` and `scripts/benchmark/reporter.py` — reused for F1/FPR deltas, trajectory summaries, and run artifacts.
- `skills/model-scores.yml` — updated from accepted runs to keep best-per-skill-model snapshots aligned with benchmark truth.
- `skills/tuning/skill-optimizer.md`, `skills/tuning/benchmark-runner.md`, `skills/tuning/local-calibration.md` — updated to reflect automated scheduled operation and safety gates.
- `.github/agents/*.md` — used as the repository’s agentic execution policy for apply/verify behavior during automated runs.

### New Components
- `.github/workflows/autoresearch-tuning.yml` — primary scheduled/dispatch workflow for orchestration.
- `.github/workflows/autoresearch-promote.yml` — reusable workflow for gated commit/PR creation and rollback handling.
- `scripts/tune/orchestrator.py` — matrix planner and loop coordinator for skill × model runs.
- `scripts/tune/history.py` — append-only trajectory writer/reader.
- `scripts/tune/config.yaml` — tuning policy (targets, max rounds, convergence, mutation budget, promotion thresholds).
- `tune-history/<skill>/<model>.jsonl` — immutable run history (baseline metrics, candidate metrics, acceptance decision, commit/PR refs).

## Technical Decisions

### Decision: Use GitHub Agentic Workflows as the Run Scheduler

**Chosen:** Trigger autoresearch via GitHub workflows (`schedule`, `workflow_dispatch`, and path-based triggers on `evals/**` and `skills/**`) and execute tuning in CI.
**Alternatives considered:**
- Local cron on a maintainer machine — rejected because it is not reproducible, not auditable, and not resilient to maintainer downtime.
- External orchestrator (Airflow/Temporal) — rejected because it adds operational overhead without additional value at current scale.

**Rationale:** Repository-native workflows give auditable runs, branch protections, deterministic artifacts, and direct integration with PR-based promotion while matching the existing `.github/agents` operating model.

### Decision: Optimize at Skill × Model Granularity

**Chosen:** Plan and run tuning per `(skill, model)` pair, not per skill globally.
**Alternatives considered:**
- Per-skill only (single shared prompt across models) — rejected because model behavior differs materially and causes cross-model regressions.
- Global monolithic tuning run — rejected because failures are harder to attribute and promotion risk is higher.

**Rationale:** Skill × model optimization aligns with the existing benchmark matrix and preserves model-specific gains while keeping diffs small and attributable.

### Decision: Two-Stage Candidate Evaluation with Hard Promotion Gates

**Chosen:** Use a fast screen on known failing cases followed by full benchmark validation; promote only if thresholds are met and no critical regression is introduced.
**Alternatives considered:**
- Promote on single full-run pass-rate increase — rejected because pass-rate alone can hide false-positive regressions.
- Promote best mutation from each round unconditionally — rejected because it can drift quality over time.

**Rationale:** Two-stage evaluation controls cost while preserving correctness. Promotion requires measurable improvement (`F1` gain and/or `FPR` reduction per policy), explicit non-regression constraints, and repeatable metric evidence.

### Decision: Append-Only Trajectory History as the Source of Improvement Truth

**Chosen:** Persist every run and decision in `tune-history/...jsonl`, then derive trend/report views from those records.
**Alternatives considered:**
- Keep only latest scores in `skills/model-scores.yml` — rejected because it loses decision rationale and trend visibility.
- Store history only in workflow logs/artifacts — rejected because artifacts expire and are harder to diff/version.

**Rationale:** Append-only history provides long-term auditability, enables trend analysis, and supports rollback/diagnosis without relying on ephemeral CI data.

### Decision: Branch-First Safety and Auto-Revert on Post-Promotion Regression

**Chosen:** All accepted mutations are committed to an automation branch and promoted via PR; merged regressions trigger automatic revert PR creation.
**Alternatives considered:**
- Direct commits to `main` from CI — rejected because it bypasses review and makes recovery risky.
- Manual rollback only — rejected because it violates the tuning safety requirement for automatic degradation handling.

**Rationale:** Branch-first promotion plus automated revert keeps the loop safe, reviewable, and compliant with required guardrails (including mandatory manual review labels for large prompt diffs).

## Data Flow

1. **Trigger:** `autoresearch-tuning.yml` starts from weekly schedule, manual dispatch, or relevant path changes.
2. **Plan:** `orchestrator.py` builds the skill × model matrix from config and current benchmark inventory.
3. **Baseline:** Runner/scorer load current benchmark metrics for each pair and write run metadata.
4. **Analyze:** Failure clusters are extracted from assertion-level outputs.
5. **Mutate:** `mutator.py` generates bounded candidate variants from failure clusters.
6. **Screen:** Candidates are evaluated on failing-case subsets; low performers are discarded.
7. **Validate:** Top candidate is run against full eval coverage for the same pair.
8. **Gate:** Policy engine checks metric deltas, non-regression constraints, and diff-size safety rules.
9. **Persist:** `history.py` appends the full decision record and updates score snapshots for accepted variants.
10. **Promote:** Promotion workflow opens/updates PR with metric delta summary; on post-merge regression detection, auto-revert PR is opened.

## API Changes

No external service API changes.

CLI/interface extensions (non-breaking) are introduced for tuning orchestration:
- `scripts/tune/autoresearch.py`: policy inputs (`--max-rounds`, `--convergence-rounds`, `--min-f1-delta`, `--max-fpr-regression`, `--history-file`, `--dry-run`).
- `scripts/tune/orchestrator.py`: matrix/run controls (`--skills`, `--models`, `--trigger`, `--config`, `--run-id`).
- Workflow dispatch inputs: target skills/models, promotion mode, and safety override flags for maintainer-only reruns.

## Dependencies

- No new Python runtime dependencies are required beyond the existing tuning/benchmark stack.
- New operational dependency: GitHub Actions workflows with permissions for `contents: write` and `pull-requests: write`.
- Optional workflow helper action for PR creation (e.g., `peter-evans/create-pull-request`) may be used as workflow infrastructure.

## Migration / Backwards Compatibility

- Existing manual tuning commands remain valid; automation wraps, not replaces, the current CLI paths.
- `skills/model-scores.yml` remains the compatibility surface for downstream consumers; history files add depth without changing consumers.
- Repositories using local calibration can continue overlay evals; orchestrator merges local calibration inputs when present and falls back to global evals otherwise.
- Rollout is opt-in via workflow file presence and repository settings, so existing behavior is preserved until enabled.

## Testing Strategy

- **Autoresearch Tuning Approach:** integration test validating benchmark → mutate → re-benchmark → gated promote sequence, plus idempotent rerun with unchanged inputs.
- **Skill Optimizer:** unit tests for failure-pattern clustering, strategy selection, and deterministic candidate ranking.
- **Benchmark Runner + Assertion Checking:** contract tests ensuring filtered execution and assertion-level logs remain authoritative for gating.
- **Local Calibration:** integration test verifying local eval overlays alter acceptance outcomes only for targeted repo patterns.
- **Performance Reporting:** reporter tests asserting trajectory tables and delta summaries map to stored history records.
- **Tuning Safety:** workflow-level tests for branch-only writes, large-diff manual-review labeling, regression-triggered auto-revert, and no-merge on threshold failures.

## Edge Cases

- **No improving mutation in all rounds:** run is recorded as no-op with explicit reason; no commit/PR is created.
- **Metric conflict (F1 up, FPR worsens):** policy gate rejects unless within configured non-regression tolerance.
- **Judge variance/flaky outcomes:** run uses repeated scoring on borderline candidates before promotion decision.
- **Concurrent workflow collisions on same skill × model:** concurrency groups serialize runs per pair to avoid branch/history races.
- **Eval drift during run:** run snapshots input hashes at start; any mismatch invalidates promotion and marks run stale.
- **Large mutation diffs (> configured line threshold):** candidate can be benchmarked but promotion is blocked pending manual review.
- **Workflow permission failure (no write/PR scope):** run still emits artifacts/history but promotion step is skipped with explicit failure status.
