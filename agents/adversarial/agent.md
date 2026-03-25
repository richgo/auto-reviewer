# Adversarial Agent

Run adversarial review flows using role-based debate and confidence-bucket outputs.

## Contract Boundary

- adversarial orchestration is a skill-level wrapper that delegates analysis to composed skills.
- subagent delegation is supported, but delegated scopes MUST remain attributable to skill outputs.
- contracts MUST NOT rely on legacy task-first or other alternate atomic primitives.

## Commands

- `adversarial-review`: run a detector -> challenger -> defender -> judge debate cycle.
- `adversarial-resume`: resume an in-progress run using stored local state.
- `adversarial-cleanup`: perform post-merge cleanup for local adversarial artifacts.

## Stage Model Configuration Contract

- adversarial config MUST allow different models per stage.
- supported stage keys: `detector`, `challenger`, `defender`, `judge`.
- each stage may define either a single model or an ordered fallback list.
- if a stage model is unavailable, use that stage's fallback list; if still unavailable, mark run degraded and continue baseline flow.
- config MUST support one reviewer per skill/concern assignment for detector stage.

Example:

```yaml
config:
  adversarial:
    db_path: .auto-reviewer/adversarial.db
    models_by_stage:
      detector: [gpt-5.3-codex, claude-sonnet-4.6]
      challenger: [claude-sonnet-4.6]
      defender: [gpt-5.3-codex]
      judge: [claude-opus-4.6, gpt-5.3-codex]
```

## Role Protocol

- detector: produce candidate findings for the target diff.
- challenger: challenge findings from other models.
- defender: defend challenged findings with evidence.
- judge: arbitrate unresolved findings.

### Round Order

`detector -> challenger -> defender -> judge`

## Output Contract

- `high-confidence`: findings with strong consensus.
- `contested`: findings requiring human review.
- `debunked`: findings rejected by adversarial debate.
- output attribution is required: each finding must include contributing skill attribution.

## SQLite Persistence Contract

- database path: `.auto-reviewer/adversarial.db`
- required tables: `runs`, `stage_tasks`, `reviewers`, `findings`, `stances`, `verdicts`, `run_events`, `cleanup_events`
- resume key: `repo, pr, commit_sha`
- transaction boundary: each stage write (task + reviewer status + outputs) is committed as a transaction
- all review workflow state MUST be persisted before stage completion is acknowledged
- one reviewer per skill/concern is required and enforced by uniqueness on `(run_id, concern_id)`

### Required Schema (SQLite DDL)

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,
  repo TEXT NOT NULL,
  pr TEXT NOT NULL,
  commit_sha TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','in_progress','paused','completed','degraded','failed')),
  degraded_reason TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE (repo, pr, commit_sha)
);

CREATE TABLE IF NOT EXISTS stage_tasks (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  stage TEXT NOT NULL CHECK (stage IN ('detector','challenger','defender','judge')),
  status TEXT NOT NULL CHECK (status IN ('pending','running','blocked','completed','failed')),
  assigned_model TEXT NOT NULL,
  attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  started_at TEXT,
  completed_at TEXT,
  error_message TEXT,
  UNIQUE (run_id, stage)
);

CREATE TABLE IF NOT EXISTS reviewers (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  concern_id TEXT NOT NULL,
  stage TEXT NOT NULL CHECK (stage IN ('detector','challenger','defender','judge')),
  model TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','running','completed','failed','skipped')),
  last_heartbeat_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE (run_id, concern_id)
);

CREATE TABLE IF NOT EXISTS findings (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  concern_id TEXT NOT NULL,
  fingerprint TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('critical','high','medium','low')),
  file_path TEXT NOT NULL,
  line INTEGER,
  detector_reviewer_id TEXT REFERENCES reviewers(id) ON DELETE SET NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (run_id, fingerprint)
);

CREATE TABLE IF NOT EXISTS stances (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  finding_id TEXT NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
  reviewer_id TEXT NOT NULL REFERENCES reviewers(id) ON DELETE CASCADE,
  stage TEXT NOT NULL CHECK (stage IN ('challenger','defender')),
  stance TEXT NOT NULL CHECK (stance IN ('support','challenge','neutral')),
  evidence_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verdicts (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  finding_id TEXT NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
  judge_reviewer_id TEXT REFERENCES reviewers(id) ON DELETE SET NULL,
  bucket TEXT NOT NULL CHECK (bucket IN ('high-confidence','contested','debunked')),
  consensus_score REAL CHECK (consensus_score >= 0 AND consensus_score <= 1),
  rationale_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (run_id, finding_id)
);

CREATE TABLE IF NOT EXISTS run_events (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  stage TEXT CHECK (stage IN ('detector','challenger','defender','judge')),
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cleanup_events (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  action TEXT NOT NULL CHECK (action IN ('archive_summary','purge_artifacts','prune_rows','vacuum')),
  status TEXT NOT NULL CHECK (status IN ('started','completed','failed')),
  details_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

### Required Status Tracking

- `runs.status`: `pending | in_progress | paused | completed | degraded | failed`
- `stage_tasks.status`: `pending | running | blocked | completed | failed`
- `reviewers.status`: `pending | running | completed | failed | skipped`
- on connection/provider interruption, current task/reviewer status MUST be left durable in DB and resumed by `adversarial-resume` without duplicate reviewer assignment.

### Strict Adherence Rules

- always enable `PRAGMA foreign_keys = ON` before any writes.
- `adversarial-review` and `adversarial-resume` MUST run each stage in a single transaction (`BEGIN IMMEDIATE ... COMMIT`), including:
  - stage task status transition
  - reviewer status transition
  - stage outputs (`findings`/`stances`/`verdicts`)
  - corresponding `run_events`
- never mark a stage `completed` unless all required rows for that stage are committed.
- never mark `runs.status = completed` unless all four `stage_tasks` are `completed` and every non-skipped reviewer is terminal (`completed` or `failed`).
- retries MUST be idempotent:
  - use UPSERT keyed by declared UNIQUE constraints
  - never create duplicate `reviewers (run_id, concern_id)` rows
  - never create duplicate `stage_tasks (run_id, stage)` rows
  - never create duplicate `findings (run_id, fingerprint)` rows
  - never create duplicate `verdicts (run_id, finding_id)` rows
- on interruption/reconnect:
  - set abandoned `running` rows to `pending` or `blocked` with a `run_events` record before resume execution
  - resume from first non-completed stage in canonical order: detector -> challenger -> defender -> judge
- any schema or constraint violation MUST fail the run explicitly (`runs.status = failed` or `degraded`) and emit a structured `run_events` error record; no silent recovery.

## Canonical Finding and Consensus Routing

- normalize each finding into a canonical record before challenge/defense rounds.
- generate a deterministic fingerprint for each canonical finding to cluster duplicates.
- use SQL aggregation over `findings`, `stances`, and `verdicts` for routing.
- route findings into: `high-confidence`, `contested`, `debunked`.
