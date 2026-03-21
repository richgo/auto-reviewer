# Tasks: Phase 5 Adversarial Engine

> Note: `openspec/changes/phase-5-adversarial-engine/specs/` is not present yet. These tasks map to the approved design decisions and proposal scope, and should be cross-referenced to concrete spec scenarios when the spec deltas are added.

## Phase 1: Agent Contract and Local Persistence Foundations

- [x] **1.1** Create adversarial agent entry instructions  
  Add `agents/adversarial/agent.md` with `adversarial-review`, `adversarial-resume`, and `adversarial-cleanup` command flow, role order (detector/challenger/defender/judge), and confidence-bucket output contract. (Design: Agent.md-Only Orchestration; Fixed Four-Role Debate Protocol)

- [x] **1.2** Define SQLite persistence contract for debate state  
  In `agents/adversarial/agent.md`, define local DB path, required tables/keys (`runs`, `findings`, `stances`, `verdicts`, cleanup tracking), resume key semantics, and transaction boundaries for deterministic reruns. (Design: SQLite as Local Source of Truth)

- [x] **1.3** Add adversarial runtime config and local artifact ignore rules  
  Update `apm.yml` with additive `config.adversarial` defaults (panel size, round limits, db path, retention policy) and update `.gitignore` to exclude `.auto-reviewer/adversarial.db` plus transient artifact directories. (Design: API Changes + Migration/Backwards Compatibility)

- [x] **1.4** Add explicit post-merge cleanup contract  
  Create `agents/adversarial/cleanup.md` (or equivalent section in `agents/adversarial/agent.md`) defining merge-triggered archive/purge flow, stale-row pruning, and idempotent SQLite vacuum behavior. (Design: Mandatory Post-Merge Cleanup)

## Phase 2: Orchestrator/Output Integration and Routing Rules

- [x] **2.1** Wire review orchestrator skill to adversarial mode handoff  
  Update `skills/core/review-orchestrator.md` to call adversarial commands, pass run identity inputs, and require explicit degraded-status metadata when fallback is used. (Design: Augment Existing Review Path with Explicit Fallback)

- [x] **2.2** Define canonical finding fingerprint and SQL consensus routing rules  
  Extend `agents/adversarial/agent.md` with canonical finding fields, fingerprinting rules, and deterministic SQL-backed routing to `high-confidence`, `contested`, and `debunked` buckets. (Design: SQL-Backed Consensus and Confidence Routing)

- [x] **2.3** Update review report output contract for adversarial metadata  
  Update `skills/outputs/review-report.md` templates/examples to include confidence class, consensus score, and compact challenge/defense summary sections while keeping existing report structure stable. (Design: Components Affected outputs + Backwards Compatibility)

- [x] **2.4** Update inline comments output contract for adversarial metadata  
  Update `skills/outputs/inline-comments.md` so inline findings include confidence indicator and short debate rationale without breaking existing platform comment payload conventions. (Design: Components Affected outputs)

- [x] **2.5** Document adversarial run/resume/cleanup lifecycle  
  Update `README.md` with adversarial command usage, SQLite storage location, retention/cleanup behavior, and fallback expectations for insufficient quorum/provider failures. (Design: Components Affected docs + Edge Cases)

## Phase 3: Testing & Verification

- [x] **3.1** Write unit tests for adversarial agent contract and SQLite schema rules  
  Add tests under `scripts/tests/adversarial/` to validate required agent commands, round ordering, required SQL schema elements, confidence bucket definitions, and cleanup idempotency clauses.

- [x] **3.2** Write integration tests for run → resume → cleanup flow  
  Add fixture-driven integration tests using temporary SQLite DB/artifact paths to verify run creation, resume by `(repo, pr, commit_sha)`, deterministic verdict materialization, and post-merge purge/retention behavior.

- [x] **3.3** Write output compatibility tests for confidence rendering  
  Add tests asserting `review-report` and `inline-comments` render adversarial metadata (`confidence`, `consensus`, debate summary) while preserving existing legacy-required fields and ordering.

- [x] **3.4** Manual verification  
  Run an adversarial review on a sample diff, inspect SQLite state transitions across rounds, re-run via resume to confirm non-duplication, simulate merge cleanup to confirm purge/prune/vacuum behavior, and validate degraded fallback output when quorum or provider checks fail.
