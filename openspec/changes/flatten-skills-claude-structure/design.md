# Design: Flatten Skills to Claude Structure

## Overview

This change standardizes skill identity around Claude’s folder-based contract: each active skill is represented by one folder named after the canonical skill identifier, with a single `SKILL.md` entry file. The design focuses on identity normalization, strict legacy cutover, duplicate merge governance, and explicit manual conflict reporting. It does not introduce new review capabilities.

## Architecture

### Components Affected
- `skills/` corpus structure and canonical naming boundaries.
- `scripts/compose/` policy, selection, and validation assumptions about skill paths.
- `scripts/benchmark/runner.py` and `scripts/tune/orchestrator.py` discovery assumptions.
- `scripts/skills/` path emission and lineage references.
- `agents/composer/agent.md` and related contracts that reference skill paths.
- `README.md` and OpenSpec capability deltas that describe active skill shape.

### New Components
- Canonicalized OpenSpec deltas for `skills` and `agent-composition` in this change folder.
- `tasks.md` execution plan for restructuring, conflict handling, and contract verification.

## Technical Decisions

### Decision: Canonical Skill Identity is Folder Name + `SKILL.md`

**Chosen:** Active skill identity resolves from `<canonical-skill-name>/SKILL.md`.

**Alternatives considered:**
- Keep existing `skills/<group>/<skill>.md` file identity — rejected because it conflicts with Claude’s documented structure.
- Support both folder and file forms indefinitely — rejected because dual identity contracts create drift and ambiguous discovery behavior.

**Rationale:** A single contract removes identity ambiguity and allows composition/validation/routing to converge on one stable reference model.

### Decision: Flatten Nested Lineage into Explicit Canonical Names

**Chosen:** Nested lineage is represented as flattened identifiers (for example `api-design/mobile` -> `api-design-mobile`).

**Alternatives considered:**
- Preserve nested runtime folders — rejected because active runtime identity would still depend on hierarchical path semantics.
- Hash- or ID-based names — rejected because they reduce readability and lineage interpretability.

**Rationale:** Flattened names preserve meaning while satisfying folder-per-skill constraints and simplifying dependency references.

### Decision: Duplicate Name Targets Merge into One Canonical Skill

**Chosen:** If multiple artifacts resolve to one canonical name, active state is one folder and one authoritative `SKILL.md`.

**Alternatives considered:**
- Keep competing duplicates and select at runtime — rejected because runtime behavior becomes non-deterministic.
- Namespace all duplicates permanently — rejected because it preserves overlap instead of canonicalizing ownership.

**Rationale:** Canonical single ownership is required for predictable composition, scoring, and attribution.

### Decision: Strict Cutover, No Legacy Path Support

**Chosen:** Active contracts reject legacy skill-path aliases once canonicalization is applied.

**Alternatives considered:**
- Transitional alias support — rejected by scope decision and because aliases prolong ambiguity.
- Best-effort silent translation — rejected because hidden remapping obscures errors and complicates validation.

**Rationale:** Explicit rejection of legacy forms keeps behavior deterministic and makes migration issues visible.

### Decision: Manual Conflict Reporting for Non-Mergeable Cases

**Chosen:** Conflicts that cannot be safely merged are surfaced as explicit manual-fix errors with skill context.

**Alternatives considered:**
- Auto-resolve all conflicts — rejected because automatic merging may cause semantic loss.
- Block without diagnostics — rejected because maintainers need actionable conflict context.

**Rationale:** Visibility-first conflict reporting protects correctness while preserving migration progress.

## Data Flow

1. Existing skill artifacts are mapped to canonical flattened identifiers.
2. Canonical identity checks detect duplicates, naming divergences, and non-mergeable conflicts.
3. Mergeable duplicates are represented by one canonical skill folder and one authoritative `SKILL.md`.
4. Composition/discovery/validation contracts resolve only canonical skill identities.
5. Legacy references in active paths fail validation with explicit errors.
6. Manual-fix error reports enumerate unresolved conflicts for maintainer action.

## API Changes

No external service API changes.

Internal contract changes:
- Active skill discovery contract changes from file-based discovery to folder + `SKILL.md`.
- Composition/validation contracts require canonical skill identities and reject legacy references.
- Output attribution contract references canonical skill identifiers.

## Dependencies

No new runtime dependencies are required. Existing repository tooling is updated to align with canonical skill identity assumptions.

## Migration / Backwards Compatibility

- This change intentionally removes active legacy path compatibility.
- Historical lineage is non-normative.
- Compatibility risk is managed through explicit validation failures and manual conflict reporting rather than alias layers.

## Testing Strategy

- **Canonical structure tests:** Validate all active skills resolve to folder + `SKILL.md` (specs: `skills` Canonical Skill Folder Contract).
- **Name flattening tests:** Validate nested lineage resolves to expected flattened identifiers (specs: `skills` Flattened Name Resolution).
- **Duplicate merge tests:** Validate a single canonical artifact per flattened identifier (specs: `skills` Canonical Duplicate Merge, Front Matter Consolidation).
- **Legacy rejection tests:** Validate composition/routing/validation reject legacy paths with explicit errors (specs: `agent-composition` Legacy Reference Rejection, Canonical Dependency Resolution).
- **Discovery tests:** Validate compose/tune/benchmark discover canonical folder-based skills only (specs: `agent-composition` Canonical Skill Discovery Contract).
- **Manual conflict reporting tests:** Validate non-mergeable conflicts surface actionable manual-fix errors (specs: `skills` Non-Mergeable Content Conflict).

## Edge Cases

- Flattened identifier collision across unrelated sources.
- Canonical name divergence (`data` lineage vs `data-integrity` active skill ownership).
- Duplicate sources with incompatible front matter semantics.
- Residual legacy path references in composer policy/tests/docs.
- Partial migration where some tools still assume `*.md` category files.

