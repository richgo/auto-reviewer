# Adversarial Post-Merge Cleanup Contract

## Trigger

- run cleanup after merge is detected for a tracked adversarial run.

## Required Actions

1. archive lightweight run summary metadata for audit.
2. purge transient round artifacts from `.skill-machine/adversarial-artifacts/`.
3. prune stale rows based on configured retention rules.
4. vacuum the sqlite database to reclaim space.

## Safety Rules

- cleanup must be idempotent and safe to re-run.
- cleanup must not remove active, non-merged run state.
