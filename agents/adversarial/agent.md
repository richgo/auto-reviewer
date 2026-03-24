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

- database path: `.skill-machine/adversarial.db`
- required tables: `runs`, `findings`, `stances`, `verdicts`, `cleanup_events`
- resume key: `repo, pr, commit_sha`
- transaction boundary: each debate round write is committed as a transaction

## Canonical Finding and Consensus Routing

- normalize each finding into a canonical record before challenge/defense rounds.
- generate a deterministic fingerprint for each canonical finding to cluster duplicates.
- use SQL aggregation over `findings`, `stances`, and `verdicts` for routing.
- route findings into: `high-confidence`, `contested`, `debunked`.
