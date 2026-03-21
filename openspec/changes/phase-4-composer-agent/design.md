# Design: Phase 4 Composer Agent

## Overview

Phase 4 adds a Composer capability that analyzes a repository and generates an `apm.yml` with the right auto-reviewer skill dependencies and version refs. The design intentionally evaluates a lightweight `agent.md`-driven generation path and adopts it as the UX entrypoint, while enforcing deterministic policy/validation so outputs remain reproducible. This keeps composition simple for users while still meeting pinning, monorepo, and update safety goals described by the Phase 4 change scope.

## Architecture

### Components Affected
- `apm.yml` — generated or merged in-place with composer-managed auto-reviewer dependencies.
- `skills/core/*.md`, `skills/concerns/*.md`, `skills/languages/*.md`, `skills/outputs/*.md` — source inventory that composition references.
- `README.md` / packaging docs — updated to describe compose/update/install workflow.
- `apm.lock.yaml` (consumer-side behavior) — remains downstream lock authority after `apm install`.

### New Components
- `agents/composer/agent.md` (or equivalent runtime agent instruction) — minimal compose entrypoint that drives repo scan and manifest drafting.
- `scripts/compose/policy.yaml` — declarative mapping from repo signals to skill dependencies.
- `scripts/compose/validator.py` — deterministic validation/normalization of generated manifest content.
- `scripts/compose/merge.py` — scoped merge logic for `apm.yml` updates.
- `scripts/tests/compose/*` — tests for policy mapping, validator behavior, merge semantics, and monorepo fixtures.

## Technical Decisions

### Decision: Agent.md-First Composition Entry

**Chosen:** Use a simple `agent.md` as the primary user-facing mechanism to generate `apm.yml`, with deterministic policy + validator backing it.
**Alternatives considered:**
- Build only a dedicated CLI composer binary/script — rejected because it adds onboarding friction when an agent-first flow is sufficient for authoring.
- Use agent-only free-form generation with no validator — rejected because it is too non-deterministic for reproducible manifests.

**Rationale:** A simple agent can generate `apm.yml` quickly and aligns with the project’s agent-centric workflow, but reliability requires deterministic guardrails.

### Decision: Declarative Signal-to-Skill Policy

**Chosen:** Keep mapping rules in `policy.yaml` instead of embedding selection logic only in prompts.
**Alternatives considered:**
- Prompt-embedded mapping tables only — rejected because policy drift and reviewability are poor.
- Hardcoded mapping in code — rejected because policy updates become unnecessarily expensive.

**Rationale:** Declarative policy keeps selection transparent, testable, and easy to evolve without rewriting agent instructions.

### Decision: Fail-Closed Validation Before Write

**Chosen:** Validate generated manifests against schema and repository skill inventory; reject write on invalid refs/paths/shape.
**Alternatives considered:**
- Best-effort write with warnings — rejected because partially incorrect manifests break install flows later.
- Silent normalization of unknown entries — rejected because hidden mutation is hard to trust.

**Rationale:** Fail-closed behavior preserves trust in generated manifests and keeps errors actionable at compose time.

### Decision: In-Place Scoped Merge for Updates

**Chosen:** `--update` replaces only composer-managed auto-reviewer dependencies while preserving unrelated dependencies and existing config keys.
**Alternatives considered:**
- Full overwrite of `apm.yml` — rejected because it can destroy user-owned settings.
- Always produce separate generated file — rejected because it complicates standard `apm install` usage.

**Rationale:** Scoped merge keeps updates safe and minimizes churn in user-managed manifest content.

### Decision: Stable-Tag Default Pinning with Explicit Overrides

**Chosen:** Default refs to stable semver tag, with explicit override options for commit SHA, branch, or no ref.
**Alternatives considered:**
- Default `#main` — rejected because manifest behavior changes over time without review.
- No refs by default — rejected because reproducibility depends on lock timing and environment.

**Rationale:** Stable defaults provide predictable installs while preserving flexibility for advanced users.

## Data Flow

1. User invokes Composer through the agent entrypoint (compose or compose-update mode).
2. Agent scans repository signals (languages, platforms, framework/build/CI hints), including subdirectories for monorepo coverage.
3. Agent asks policy resolver for required core, concern, language, and output skills.
4. Resolver returns normalized dependency set with deterministic ordering.
5. Ref strategy applies version pins (tag/sha/branch/none) to each dependency path.
6. Existing `apm.yml` (if present) is loaded; merge layer replaces only composer-managed dependency slice.
7. Validator enforces schema shape, known skill paths, and valid ref format; if invalid, write is aborted with errors.
8. Valid manifest is written, then user runs `apm install`/`apm compile`; lockfile resolution remains APM-owned.
9. On repo changes, the same flow reruns in update mode and refreshes only managed entries.

## API Changes

No external service API changes.

Composer introduces an internal composition interface:
- Agent mode: compose command in `agent.md` (initial generation) and compose-update (merge refresh).
- Validation/merge helpers with non-breaking manifest behavior:
  - deterministic ordering of composer-managed `dependencies.apm` entries,
  - optional metadata comments for generation source and detected stack summary,
  - `compilation.strategy: distributed` when multi-path stacks are detected.

## Dependencies

- No new runtime dependencies are required beyond existing YAML tooling.
- Operational dependency: APM CLI for downstream install/compile (`apm install`, `apm compile`).
- Repository dependency: stable git refs/tags for `richgo/auto-reviewer` to support default pin strategy.

## Migration / Backwards Compatibility

- Existing manual `apm.yml` files remain compatible; compose-update preserves user-owned non-composer sections.
- Existing consumers can adopt composer incrementally by generating once and reviewing dependency diffs.
- No storage/data migration is required; lockfile lifecycle is unchanged.
- Invalid existing YAML is handled as explicit failure (no partial overwrite).

## Testing Strategy

- Policy mapping tests using fixture repos for single-stack, mixed-stack, and monorepo layouts.
- Validator tests for malformed YAML, unknown skill path, invalid ref syntax, and deterministic ordering.
- Merge behavior tests to ensure non-composer keys are preserved during update mode.
- Agent contract tests (prompt-to-manifest fixtures) to verify agent.md generation stays within policy boundaries.
- End-to-end fixture tests: compose → validate → write → dry-run `apm install` shape checks (no review execution).

## Edge Cases

- **Agent hallucinated dependency path:** validator rejects and reports nearest known skill path.
- **Ambiguous platform detection:** include union of candidate platform skills rather than selecting one heuristically.
- **Very large monorepo:** bounded scan with ignore patterns to avoid runaway analysis time.
- **Conflicting pin directives:** explicit per-run override takes precedence, conflict surfaced in output notes.
- **User manually reordered managed dependencies:** deterministic normalization reapplies order on update.
- **No detectable stack signals:** fallback manifest contains required core baseline plus explicit warning note.
