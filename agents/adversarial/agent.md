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

### Required Status Tracking

- `runs.status`: `pending | in_progress | paused | completed | degraded | failed`
- `stage_tasks.status`: `pending | running | blocked | completed | failed`
- `reviewers.status`: `pending | running | completed | failed | skipped`
- on connection/provider interruption, current task/reviewer status MUST be left durable in DB and resumed by `adversarial-resume` without duplicate reviewer assignment.

## Canonical Finding and Consensus Routing

- normalize each finding into a canonical record before challenge/defense rounds.
- generate a deterministic fingerprint for each canonical finding to cluster duplicates.
- use SQL aggregation over `findings`, `stances`, and `verdicts` for routing.
- route findings into: `high-confidence`, `contested`, `debunked`.
