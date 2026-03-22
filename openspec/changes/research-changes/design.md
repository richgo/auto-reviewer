# Design: Research Changes

## Overview

This change formalizes a flattened architecture where skills are the only atomic review primitive and agents are composition/execution wrappers over skills. The design migrates review-task guidance into the skill layer, retires task-first runtime assumptions, and aligns composition/tuning/benchmark behavior with what runtime tooling already does today. The result is a single canonical layer for review guidance, evaluation linkage, and model tuning.

## Architecture

### Components Affected
- `review-tasks/` — transitioned from active architecture primitive to migration source, then retired from runtime dependency paths.
- `skills/` (`concerns/`, `languages/`, `core/`, `outputs/`, `tuning/`) — canonical review guidance and coverage surface.
- `evals/` — canonical skill-linked eval datasets.
- `scripts/tune/orchestrator.py` and `.github/workflows/autoresearch-tuning.yml` — existing skill-scoped tuning semantics used as the normative contract.
- `scripts/benchmark/runner.py` — existing skill/eval discovery semantics used as the normative benchmark contract.
- `scripts/compose/policy.yaml` and composition docs — explicit skill dependency composition model.
- `agents/composer/agent.md`, `agents/adversarial/agent.md` — explicit agent-as-skill-group contract surfaces.
- `README.md` and `openspec/specs/review-tasks/spec.md` — currently encode task-first architecture language that must be updated.
- Historical OpenSpec change docs under `openspec/changes/` that describe review-tasks as atomic.

### New Components
- `openspec/changes/research-changes/specs/skills/spec.md` — skill atomicity and ownership deltas.
- `openspec/changes/research-changes/specs/agent-composition/spec.md` — agent-as-skill-group deltas.
- `openspec/changes/research-changes/specs/review-tasks/spec.md` — modified/removed review-task deltas for flattened architecture.

## Technical Decisions

### Decision: Skills as the Only Atomic Runtime Primitive

**Chosen:** Treat skills as the only independently tuneable, benchmarkable, and executable primitive.
**Alternatives considered:**
- Keep dual primitives (review-tasks + skills) — rejected because it preserves duplicated ownership and ongoing drift between authored and executable layers.
- Keep review-tasks atomic and regenerate skills periodically — rejected because runtime tooling already resolves and reports by skill identifiers.

**Rationale:** Current tuning and benchmark flows already operate at skill granularity, so formalizing skill atomicity removes conceptual mismatch and avoids dual-source maintenance.

### Decision: Agents as Composition and Delegation Wrappers

**Chosen:** Define agents strictly as wrappers that select, group, and delegate skill execution (including subagent flows).
**Alternatives considered:**
- Keep agent contracts free-form without skill attribution — rejected because traceability and governance degrade.
- Introduce a new primitive between agents and skills — rejected because it recreates multi-layer ambiguity.

**Rationale:** Existing composition and adversarial flows already act as orchestrators over skill-oriented outputs; this decision codifies that boundary.

### Decision: Migrate Review-Task Guidance into Skills, Then Retire Task-First Contracts

**Chosen:** Migrate bug-class guidance into skill artifacts and retire standalone review-task requirements as active runtime obligations.
**Alternatives considered:**
- Leave review-tasks as permanent parallel references — rejected because it preserves split ownership for guidance and evaluation intent.
- Hard-delete review-tasks without migration mapping — rejected because it risks coverage loss and broken lineage.

**Rationale:** A migration-first retirement preserves review coverage while converging ownership to one canonical layer.

### Decision: Preserve Coverage Guarantees at Skill Layer

**Chosen:** Re-home concern/platform/security-reference guarantees in the skill layer after migration.
**Alternatives considered:**
- Preserve exact review-task count obligations in active specs — rejected because count-based task inventory is tied to a retired primitive.
- Drop explicit coverage guarantees — rejected because regression detection becomes subjective.

**Rationale:** Flattening should simplify primitives, not weaken coverage accountability.

### Decision: Keep Existing Runtime Entry Points and Make Spec/Doc Contracts Match Them

**Chosen:** Use current code paths as the normative architectural baseline and align spec/doc language to match.
**Alternatives considered:**
- Introduce new runtime control planes as part of this change — rejected because proposal scope excludes runtime refactors.
- Delay alignment until a later feature phase — rejected because current mismatch already causes confusion.

**Rationale:** This change is principally contract and architecture alignment; using existing behavior minimizes risk.

## Data Flow

1. Migration input is read from existing review-task guidance and mapped into skill-level guidance ownership.
2. Skill artifacts become the canonical source for review instructions and reference mappings.
3. Eval datasets resolve by skill identifier and are consumed by benchmark/tuning workflows.
4. Tuning workflows enumerate skill × model pairs and persist score trajectories keyed by skill identifiers.
5. Benchmark workflows discover skill/eval pairs and emit model × skill score outputs.
6. Composition workflows select dependencies as skill paths and emit agent-ready manifests.
7. Agent orchestration routes execution over selected skills and emits outputs attributable to participating skills.

## API Changes

No external service API changes.

Internal contract changes:
- OpenSpec requirement ownership shifts from task-first to skill-first for active runtime semantics.
- Agent contract semantics are tightened to skill-group composition and skill-attributable output routing.
- Review-task capability contract is reduced to transitional migration semantics and no longer defines active runtime requirements.

## Dependencies

No new dependencies.

The design relies on existing repository components and workflows:
- skill-scoped tuning and benchmark scripts,
- existing composition policy/agent contracts,
- current OpenSpec capability structure.

## Migration / Backwards Compatibility

- Backwards compatibility is preserved at runtime because existing execution paths are already skill-first.
- Compatibility risk is documentation/spec drift during transition; migration requires synchronized updates across README, specs, and active change docs.
- Review-task retirement is migration-gated: guidance and coverage must exist in skills before task-first requirements are considered fully retired.
- Historical artifacts may continue to exist for audit context, but they are not normative for active runtime behavior.

## Testing Strategy

- **Spec conformance tests:** validate that skill/tuning/benchmark/composition contracts are expressed with skill identifiers and no standalone task requirement for execution.
- **Coverage regression checks:** verify concern/platform/security-reference coverage remains represented in skills after migration.
- **Contract alignment checks:** confirm agent/composition artifacts continue to reference skill paths and skill-attributable outputs.
- **Documentation consistency checks:** verify pipeline and architecture language no longer defines review-tasks as active atomic runtime units.
- **Migration integrity review:** perform mapping validation from prior task guidance to skill artifacts, with explicit checks for omissions.

## Edge Cases

- **Guidance bloat in skills:** migrated content may exceed practical readability; mitigation is to preserve concise skill bodies with structured references.
- **Coverage gaps during migration:** some task intent may be omitted or duplicated; mitigation is explicit migration mapping and coverage audits before retirement.
- **Ambiguous task-to-skill mapping:** one task may span multiple skills; mitigation is canonical ownership rules with cross-reference markers.
- **Legacy references in historical docs:** old phase docs may continue to imply task-first semantics; mitigation is explicit “historical/non-normative” labeling.
- **Tooling assumptions in third-party docs:** external users may rely on old terminology; mitigation is transitional compatibility notes in user-facing docs.
