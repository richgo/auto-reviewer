# Proposal: Research Changes

## Intent

The project currently has a conceptual and structural mismatch: `review-tasks/` remains a separate primitive while runtime systems already tune and score **skills**. Maintaining both layers as independent artifacts creates duplication, ambiguous ownership, and drift between what is authored, what is benchmarked, and what is composed for execution.

## Scope

### In Scope
- Reframe the primitive model so **skills** are the atomic tuneable unit.
- Define **agents** as the orchestration/grouping layer that composes skills, including subagent execution boundaries.
- Migrate all `review-tasks/` content into skill artifacts so bug classes live in one canonical layer.
- Remove the standalone `review-tasks/` taxonomy from the active architecture and align repository docs/specs accordingly.
- Align repository documentation and OpenSpec artifacts with the flattened primitive model.

### Out of Scope
- Implementing runtime refactors, new orchestration code paths, or packaging migrations.
- Rebuilding benchmark datasets or retuning existing skills.
- Altering adversarial protocol behavior beyond terminology alignment.

## Approach

Adopt a fully flattened primitive model where all review guidance and eval intent are represented at the skill layer. Consolidate duplicated task guidance into corresponding skills, then retire task-level architecture language so tuning, scoring, and composition semantics converge on a single atomic unit. Position agents strictly as compositional wrappers over skills.

## Impact

This change affects architectural and specification surfaces that currently encode task-first assumptions:
- `README.md` pipeline narrative and phase language.
- `openspec/specs/review-tasks/spec.md` requirement framing.
- `review-tasks/` content and directory role in the repository.
- Skill corpus organization under `skills/`, including concern/language coverage boundaries.
- Historical/active OpenSpec change context in `openspec/changes/` that references tasks as a separate primitive.
- Agent and composition descriptions (`agents/`, `scripts/compose/policy.yaml`).
- Tuning/scoring narrative consistency with existing skill-centric runtime behavior (`scripts/tune/orchestrator.py`, `.github/workflows/autoresearch-tuning.yml`, `scripts/benchmark/runner.py`).

## Risks

- Large-content migration may reduce clarity if skill files absorb too much detail without clear structure.
- Mapping 1:1 task intent into existing skill boundaries may introduce coverage regressions or accidental omission.
- Existing community understanding may depend on current phase language and require migration guidance.
- If boundaries are under-specified, future contributors may reintroduce parallel primitives (tasks vs skills).
- Drift risk remains if specs and docs are updated without corresponding governance conventions.

## Open Questions

- Should migrated task-level detail be embedded directly in skill bodies or relocated into skill-local references to preserve readability?
- What is the canonical contract for “agent as skill-group” (naming, metadata, and subagent invocation boundaries)?
- How should legacy phase naming be updated to preserve historical context without preserving outdated semantics?
- Do we need explicit guardrails in composition/tuning specs to prevent non-skill tuneable units from reappearing?
