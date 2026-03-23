# Proposal: Flatten Skills to Claude Structure

## Intent

The current skill corpus does not match the Claude skills contract. Active skills are mostly file-based (`skills/<group>/<skill>.md`) while migrated review-task skills exist in nested trees (`skills/review-tasks/...`). This creates conflicting skill identities, duplicate flattened names, and inconsistent ownership of metadata/content. Without one canonical folder-based model, composition, validation, benchmarking, and tuning contracts remain ambiguous.

## Scope

### In Scope
- Define a canonical, Claude-aligned skill shape: one folder per skill, folder name equals skill name, and one `SKILL.md` entry file per skill.
- Flatten nested skill folders into explicit names that preserve hierarchy semantics (for example `api-design/mobile` -> `api-design-mobile`).
- Consolidate multiple artifacts that resolve to the same flattened skill name into one canonical `SKILL.md` with updated front matter.
- Define strict cutover boundaries with no legacy/alias path support.
- Record known migration errors that require manual resolution before or during the restructure.
- Align OpenSpec and repository contracts to the normalized skill identity model.

### Out of Scope
- Implementing migration scripts or runtime code changes in this proposal.
- Defining rollout sequencing, automation details, or task-level execution steps.
- Introducing backward-compatibility layers for old skill paths.
- Changing review semantics beyond identity, placement, and canonical metadata ownership.

## Approach

Normalize the repository around a single skill contract defined by Claude docs: folder-named skills with one `SKILL.md` each. Treat flattening as an identity and governance change, not a feature addition: remove structural ambiguity, unify duplicate name targets into canonical skills, and make non-mergeable conflicts explicit as manual remediation errors.

## Impact

This change affects all surfaces that currently assume file-based skill placement or mixed naming contracts:
- `skills/` corpus layout and naming authority.
- Composer policy/selection/validation surfaces (`scripts/compose/policy.yaml`, `scripts/compose/*.py`, `agents/composer/agent.md`).
- Benchmark and tuning skill discovery assumptions (`scripts/benchmark/runner.py`, `scripts/tune/orchestrator.py`).
- Skill mapping and migration inventory outputs (`scripts/skills/migration_map.py` and related tests).
- Repository/OpenSpec documentation that currently describes category file layouts.

Known manual-fix error classes:
- Flattened-name collisions between active concern skills and review-task-derived trees (for example `api-design`, `code-quality`, `concurrency`, `correctness`, `observability`, `performance`, `reliability`, `testing`, and `security-mobile`).
- Naming divergence where semantically related coverage resolves to different flattened names (`data-integrity` vs `data` lineage) and requires explicit canonical ownership.
- Non-mergeable duplicate content conflicts where sources disagree on front matter semantics or incompatible scope boundaries.

## Risks

- Content loss or semantic drift during duplicate-name merges if boundaries are not explicit.
- Tooling failures where scripts/tests assume `*.md` skill files in category directories.
- External dependency breakage due strict no-legacy cutover of path references.
- Ambiguous ownership of front matter when multiple artifacts are merged into one canonical `SKILL.md`.
- Incomplete manual remediation of known collisions creating partial or inconsistent skill states.

## Open Questions

- None at proposal stage. Canonical decisions are fixed for this change: folder-per-skill, `SKILL.md` per skill, flattened folder-derived names, duplicate-name merge into one canonical skill, and no legacy path support.
