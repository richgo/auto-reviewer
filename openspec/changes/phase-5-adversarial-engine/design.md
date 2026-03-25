# Design: Phase 5 Adversarial Engine

## Overview

Phase 5 adopts an `agent.md`-only adversarial workflow: orchestration logic lives in agent instructions instead of a dedicated engine service or script stack. Debate state is persisted locally in SQLite to support async progress, deterministic reruns, and auditability without external infrastructure. After merge, adversarial artifacts are cleaned automatically so repository state remains lean and non-accumulative.

## Architecture

### Components Affected
- `agents/` — adds adversarial entry instructions and command contract for generate/review/cleanup lifecycle.
- `skills/core/review-orchestrator.md` — extended to call adversarial mode and consume confidence-tiered outputs.
- `skills/outputs/review-report.md` and `skills/outputs/inline-comments.md` — extended to render confidence class and debate evidence summary.
- `apm.yml` (`config.adversarial`) — controls panel size, round limits, stage-specific model mapping, and cleanup policy.
- `README.md` and usage docs — documents adversarial run lifecycle, local persistence, and merge cleanup semantics.
- `.gitignore` and local runtime conventions — ensures local DB/artifacts are never committed.

### New Components
- `agents/adversarial/agent.md` — sole orchestration surface for detector/challenger/defender/judge protocol.
- `.auto-reviewer/adversarial.db` — local SQLite state store for runs, findings, stances, and verdicts.
- `.auto-reviewer/adversarial-artifacts/` — ephemeral serialized round outputs linked from SQLite.
- `agents/adversarial/cleanup.md` (or cleanup section inside `agent.md`) — post-merge retention and purge policy contract.

## Technical Decisions

### Decision: Agent.md-Only Orchestration

**Chosen:** Implement Phase 5 as an instruction-driven workflow anchored in `agents/adversarial/agent.md` with no dedicated adversarial script runtime.
**Alternatives considered:**
- New `scripts/adversarial/*` control-plane implementation — rejected because it duplicates orchestration logic that can be expressed in agent contracts.
- External service orchestration — rejected because it adds infrastructure and operational complexity without phase-level necessity.

**Rationale:** An `agent.md`-only design matches repository conventions from prior phases, keeps behavior transparent/reviewable, and reduces moving parts.

### Decision: SQLite as Local Source of Truth

**Chosen:** Persist all debate lifecycle state in a local SQLite database under `.auto-reviewer/adversarial.db`.
**Alternatives considered:**
- JSONL file-only persistence — rejected because cross-round joins, resume semantics, and cleanup targeting are less reliable.
- Remote database (Postgres/hosted KV) — rejected because local-first operation and privacy are preferred for this phase.

**Rationale:** SQLite provides transactional durability, deterministic queryability, and zero external dependency while remaining easy to clean up post-merge.

### Decision: Fixed Four-Role Debate Protocol

**Chosen:** Use detector, challenger, defender, and judge roles with bounded rounds and deterministic ordering.
**Alternatives considered:**
- Detector-only + voting — rejected because it weakens adversarial scrutiny depth.
- Open-ended argument loops — rejected because latency/cost become difficult to bound.

**Rationale:** A fixed protocol balances quality and cost while preserving reproducible, testable behavior.

### Decision: SQL-Backed Consensus and Confidence Routing

**Chosen:** Compute confidence routing (`high-confidence`, `contested`, `debunked`) from SQL-queried stance/verdict aggregates plus configured thresholds.
**Alternatives considered:**
- Free-form judge narrative as final confidence — rejected because reproducibility and deterministic routing suffer.
- Equal-weight raw vote counting only — rejected because it underuses available model performance priors.

**Rationale:** SQL-backed aggregation makes decision logic auditable and stable across reruns while supporting transparent threshold tuning.

### Decision: Stage-Specific Model Assignment

**Chosen:** Support explicit model selection per adversarial stage (`detector`, `challenger`, `defender`, `judge`) with optional ordered fallback lists per stage.
**Alternatives considered:**
- Single model shared across all stages — rejected because stage responsibilities differ and benefit from specialized model strengths.
- Global model pool with no stage pinning — rejected because behavior is less deterministic and harder to debug/reproduce.

**Rationale:** Stage-level assignment enables role specialization while preserving deterministic reruns and clear operator control.

### Decision: Reviewer and Stage Task Durability

**Chosen:** Persist one reviewer assignment per skill/concern and explicit stage task records with statuses in SQLite, committed at each stage boundary.
**Alternatives considered:**
- Persist only aggregate run/finding rows — rejected because mid-run interruption recovery becomes lossy.
- Reconstruct reviewer/task state from logs — rejected because reconstruction is fragile and non-deterministic.

**Rationale:** Durable reviewer/task state guarantees resumability after connection failures and provides an auditable execution trail.

### Decision: Strict Schema Adherence

**Chosen:** Define a concrete SQLite schema contract (DDL, constraints, indexes) and require strict runtime adherence to those constraints.
**Alternatives considered:**
- Soft schema guidance without executable DDL — rejected because implementations drift and resume guarantees weaken.
- Application-only validation without DB constraints — rejected because invariant enforcement becomes incomplete under retries/concurrency.

**Rationale:** Hard DB constraints plus transactional stage boundaries produce deterministic behavior, stronger data integrity, and safer interruption recovery.

### Decision: Mandatory Post-Merge Cleanup

**Chosen:** Execute cleanup immediately after merge detection: archive minimal summary rows, purge heavy round artifacts, and vacuum SQLite.
**Alternatives considered:**
- Keep all history indefinitely — rejected because local state bloat and stale data accumulation become operational noise.
- Manual cleanup only — rejected because stale adversarial state is easy to forget and causes drift.

**Rationale:** Mandatory cleanup keeps local runtime state bounded and reduces accidental cross-PR contamination while preserving essential audit summaries.

### Decision: Augment Existing Review Path with Explicit Fallback

**Chosen:** Adversarial mode augments current review; on insufficient healthy models or DB issues, agent falls back to baseline review with explicit degraded-status metadata.
**Alternatives considered:**
- Hard fail adversarial runs — rejected because it would block review delivery.
- Silent fallback with no status marker — rejected because operators lose visibility into degraded quality mode.

**Rationale:** Explicit fallback preserves delivery guarantees and operator trust.

## Data Flow

1. User invokes adversarial review through `agents/adversarial/agent.md`.
2. Agent initializes/opens `.auto-reviewer/adversarial.db` and creates a `run` record keyed by repo + PR + commit SHA.
3. Agent materializes stage tasks and reviewer assignments (one reviewer per skill/concern) with `pending` status in SQLite.
4. Detector round writes normalized candidate findings into SQLite (canonical fingerprint, severity, provenance) and updates task/reviewer statuses transactionally.
5. Challenger and defender rounds append per-model stances and evidence rows linked to finding fingerprints, with status transitions persisted at each stage boundary.
6. Judge round writes arbitration outcomes for unresolved findings and final stage statuses.
7. On interruption, resume loads incomplete tasks/reviewer statuses and continues from the first non-completed stage without duplicate assignments.
8. Confidence routing query materializes final buckets (`high-confidence`, `contested`, `debunked`) and exports output payloads.
9. Output skills render confidence and debate summary into report/comment formats.
10. On merge detection, cleanup contract archives lightweight run summary, deletes transient artifacts, prunes stale DB rows, and vacuums database.

## API Changes

No external service API changes.

Internal interface updates:
- New adversarial agent command contract in `agent.md` (run, resume, cleanup).
- Additive output payload fields for confidence class, consensus score, and debate summary reference.
- Additive `apm.yml` adversarial config keys for SQLite path, retention, post-merge cleanup policy, and `models_by_stage` mapping.
- Additive SQLite entities for stage tasks and reviewer assignments with explicit statuses.
- Additive mandatory SQLite DDL and strict adherence invariants (foreign keys, uniqueness, check constraints, idempotent upserts).

## Dependencies

- No new external services.
- Runtime dependency on local SQLite (Python standard library `sqlite3`).
- Existing provider API credentials remain required for participating models.

## Migration / Backwards Compatibility

- Backwards compatible by default: non-adversarial flow is unchanged when adversarial mode is disabled.
- Existing output formats remain valid; adversarial metadata is additive.
- No historical migration required; SQLite DB is local and initialized lazily.
- Cleanup policy ensures ephemeral adversarial state does not pollute long-lived repository artifacts.

## Testing Strategy

- Agent contract tests validating command flow, role transitions, and deterministic prompt boundaries.
- SQLite schema and query tests for run state, finding clustering, consensus routing, and resume behavior.
- SQLite schema and query tests for reviewer/task status durability and one-reviewer-per-concern invariants.
- Schema contract tests that execute the documented DDL and assert all CHECK/UNIQUE/FOREIGN KEY constraints are active.
- Transaction tests verifying no partial stage completion rows are visible after simulated mid-transaction failure.
- Integration tests for end-to-end multi-round flow using mocked model responses and deterministic DB snapshots.
- Integration tests for degraded fallback paths (provider failure, quorum loss, DB lock) with explicit status assertions.
- Output compatibility tests ensuring review-report/inline-comments render confidence and debate context without regressions.
- Post-merge cleanup tests validating artifact purge, retention policy behavior, and DB vacuum/prune effects.

## Edge Cases

- **SQLite locked during concurrent runs:** agent uses bounded retry/backoff; if lock persists, run degrades with explicit status.
- **Interrupted run before verdict:** resume command reloads open run state from SQLite and continues from last completed round.
- **Interrupted run mid-stage due to connection failure:** resume reloads incomplete `stage_tasks` and `reviewers` status rows and resumes exactly once per pending/running item.
- **Conflicting duplicate findings across models:** canonical fingerprinting plus SQL clustering prevents double-reporting.
- **Judge output malformed:** routing falls back to aggregate stance thresholds and marks arbitration parse error.
- **Merge event without completed cleanup:** cleanup is idempotent and safe to re-run.
- **Retention misconfiguration (zero-day or negative window):** agent enforces safe minimum retention before purge.
- **Repository switch with stale DB path:** run key includes repo fingerprint to prevent cross-repo contamination.
- **Constraint violation during resume (duplicate reviewer/finding/verdict):** fail/degrade explicitly, record structured error event, and do not silently continue.
