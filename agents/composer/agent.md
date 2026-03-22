# Composer Agent

Generate and update `apm.yml` for a repository using deterministic, policy-constrained dependency selection.

## Contract Boundary

- composer is a **skill-group** orchestration layer and does not introduce any primitive below skills.
- composition decisions MUST delegate execution to selected skills and emitted skill paths.
- contracts MUST NOT depend on legacy task-first or alternate atomic unit semantics.

## Commands

- `compose`: analyze the target repository and generate composer-managed entries in `apm.yml`.
- `compose-update`: re-run analysis and update only composer-managed `dependencies.apm` entries while preserving non-managed sections.

## Required Inputs

- repository path to analyze
- target `apm.yml` path
- optional pin strategy override (`tag|sha|branch|none`)

## Output Contract

- generated or updated `apm.yml`
- composer-managed dependency list for auto-reviewer skills
- explicit validation errors when output violates policy/schema constraints

## Guardrails

- use composition policy mappings for skill selection
- reject invalid refs, unknown skill paths, or invalid manifest shape
- do not overwrite unrelated user-managed `apm.yml` content during updates
