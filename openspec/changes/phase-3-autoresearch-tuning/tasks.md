# Tasks: Phase 3 Autoresearch Tuning

## Phase 1: Tuning Engine Foundations

- [x] **1.1** Add tuning policy config and CLI gate inputs  
  Create `scripts/tune/config.yaml` and wire policy loading/overrides in `scripts/tune/autoresearch.py` for `--max-rounds`, `--convergence-rounds`, `--min-f1-delta`, `--max-fpr-regression`, `--history-file`, and `--dry-run`. Ensure deterministic, bounded round execution. (Design: API Changes; Decision: Two-Stage Candidate Evaluation with Hard Promotion Gates)

- [x] **1.2** Implement skill × model matrix planning  
  Create `scripts/tune/orchestrator.py` to discover skills/models, apply `--skills`, `--models`, `--trigger`, `--config`, and `--run-id` filters, and emit stable per-pair plans for downstream execution. (Design: Decision: Optimize at Skill × Model Granularity; Data Flow step 2)

- [x] **1.3** Add failure-cluster mutation constraints  
  Extend `scripts/tune/mutator.py` to cluster assertion failures and generate bounded, explainable candidates using configurable mutation budgets and diff-size accounting metadata. (Design: Components Affected mutator; Data Flow steps 4-5; Edge Case: large mutation diffs)

- [x] **1.4** Refactor autoresearch loop to two-stage evaluation  
  Update `scripts/tune/autoresearch.py` to execute baseline, failing-case screening, and full benchmark validation in order, then rank candidates deterministically and stop on convergence criteria. (Design: Decision: Two-Stage Candidate Evaluation; Data Flow steps 3, 6, 7)

- [x] **1.5** Implement policy gate and stale-input safeguards  
  Add gate checks in `scripts/tune/autoresearch.py` for F1/FPR thresholds, non-regression tolerances, repeated scoring for borderline outcomes, and input hash checks that invalidate stale promotions. (Design: Data Flow step 8; Edge Cases: metric conflict, judge variance, eval drift)

## Phase 2: History, Promotion, and Workflow Automation

- [x] **2.1** Build append-only tuning history module  
  Create `scripts/tune/history.py` for immutable JSONL append/read APIs and write records to `tune-history/<skill>/<model>.jsonl` with baseline metrics, candidate metrics, acceptance decision, and run metadata. (Design: Decision: Append-Only Trajectory History; Data Flow step 9)

- [x] **2.2** Wire accepted runs to score snapshots and reporting payloads  
  Update orchestrator/autoresearch integration to refresh `skills/model-scores.yml` only for accepted candidates and emit trajectory summary fields consumed by reporting outputs. (Design: Components Affected `model-scores.yml`, scorer/reporter; Data Flow step 9)

- [x] **2.3** Add scheduled/dispatched tuning workflow  
  Create `.github/workflows/autoresearch-tuning.yml` with weekly schedule, `workflow_dispatch` inputs, and path triggers on `evals/**` + `skills/**`; configure per-pair concurrency groups and artifact publication. (Design: Decision: GitHub Agentic Workflows as Scheduler; Data Flow step 1; Edge Case: concurrent workflow collisions)

- [x] **2.4** Add reusable promotion workflow with branch-first safety  
  Create `.github/workflows/autoresearch-promote.yml` to consume promotion metadata, commit to automation branches, open/update PRs, and enforce manual-review labeling for diffs above configured thresholds. (Design: Decision: Branch-First Safety and Auto-Revert; Data Flow step 10; Edge Case: large mutation diffs)

- [x] **2.5** Implement regression-triggered auto-revert handling  
  Extend promotion workflow jobs to detect post-merge regressions, open revert PRs automatically, and link revert rationale to stored tuning history records. (Design: Decision: Branch-First Safety and Auto-Revert on Post-Promotion Regression)

- [x] **2.6** Update tuning operation skills documentation  
  Update `skills/tuning/skill-optimizer.md`, `skills/tuning/benchmark-runner.md`, and `skills/tuning/local-calibration.md` for automated schedules, gate thresholds, PR-based promotion flow, and permission-failure behavior. (Design: Components Affected tuning docs; Migration/Backwards Compatibility)

## Phase 3: Testing & Verification

- [x] **3.1** Write unit tests for orchestrator, mutator, and policy gate  
  Add tests in `scripts/tests/tune/` for matrix planning, deterministic candidate ordering, mutation budget/diff limits, convergence stopping, and metric-conflict rejection logic. (Design Testing Strategy: Skill Optimizer + Tuning Safety; Edge Cases: no improving mutation, metric conflict)

- [x] **3.2** Write integration tests for end-to-end tuning and persistence  
  Add integration coverage for baseline → mutate → re-benchmark → gated promote flow, idempotent reruns with unchanged inputs, local calibration overlay effects, stale-run invalidation, and `tune-history` append semantics. (Design Testing Strategy: Autoresearch Tuning Approach + Local Calibration + Benchmark Runner)

- [x] **3.3** Write workflow-level safety tests  
  Add workflow tests/fixtures to verify branch-only writes, no-merge on threshold failures, mandatory manual-review labels for large diffs, serialized runs per skill × model, and regression-triggered auto-revert PR creation. (Design Testing Strategy: Tuning Safety)

- [x] **3.4** Manual verification  
  Run one dry-run and one real skill × model tuning execution; verify artifacts/history output, accepted-only `skills/model-scores.yml` updates, PR-based promotion behavior, and automatic revert PR creation under simulated regression.

## Phase 4: Multi-Model Tuning Cascade (Amendment)

- [x] **4.1** Implement cascade orchestration handler
   Create `scripts/tune/cascade.py` to coordinate multi-model escalation: run Stage 1 (gpt-5-mini, 5 iterations, 95% target), detect convergence failure, escalate to Stage 2 (claude-haiku-4.5, 3 iterations, 95% target), and route unresolved skills to needs-review workflow. (Design: Decision: Multi-Model Tuning Cascade with Escalation; Data Flow step 10+)

- [ ] **4.2** Wire cascade into orchestrator and workflow
   Update `scripts/tune/orchestrator.py` to invoke cascade handler on convergence failures; wire cascade models and iteration limits into `scripts/tune/config.yaml`; update `.github/workflows/autoresearch-tuning.yml` to handle cascade stages and pass cascade metadata through promotion workflow.

- [ ] **4.3** Implement needs-review tracking and generation
   Create `scripts/tune/needs_review.py` to generate and maintain `skills-tools/needs-review.md` with skills that failed cascade; track skill name, best model attempted, final pass rate, and tuning history link. Format as sortable checklist for manual intervention workflow.

- [ ] **4.4** Add cascade configuration and policy controls
   Extend `scripts/tune/config.yaml` with cascade sequence definition (models, iteration limits, threshold targets); add `--cascade-enabled`, `--cascade-models`, and `--max-stages` CLI overrides for testing and workflow dispatch control.

- [ ] **4.5** Test cascade orchestration end-to-end
   Write integration tests for Stage 1 → Stage 2 transition logic, convergence-failure detection, needs-review list generation, and idempotent needs-review updates. Add workflow-level tests for cascade stage concurrency and multi-stage artifact chaining.
