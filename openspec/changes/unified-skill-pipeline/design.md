# Design: Unified Skill Pipeline

## Overview

This change consolidates skill authoring into one technical pipeline with two primary lifecycle stages: `create` and `tune`. The design keeps the current skill, eval, tuning, and benchmark building blocks, but introduces a shared orchestration layer and a provider-agnostic model interface so the same workflow can run across Copilot, Claude, and Codex without duplicating pipeline logic.

The implementation direction is evolutionary rather than a rewrite. Existing scripts in `skills-tools/skill-creator/`, `scripts/tune/`, and `scripts/benchmark/` become pipeline components behind a single workflow contract, while `local-calibration` remains deliberately outside the canonical skill authoring path.

## Architecture

### Components Affected

- `skills-tools/skill-creator/` authoring and eval-loop scripts
- `scripts/tune/` tuning, cascade, scoring, mutation, and needs-review flows
- `scripts/benchmark/` benchmark execution and reporting
- duplicated model-access wrappers in skill-creator, tuning, and benchmark code
- authoring documentation in `skills-tools/creating-skills.md`

### New Components

- **Pipeline entry module** that coordinates `create` and `tune` lifecycle stages
- **Shared workflow state layer** that resolves canonical skill artifacts, linked evals, and lifecycle outputs
- **Provider-agnostic model transport layer** used by create, eval, tune, and benchmark stages
- **Eval readiness validator** that blocks weak generated eval sets from entering tuning
- **Promotion outcome record** that makes pass, gated, and manual-review outcomes explicit

## Technical Decisions

### Decision: Use one pipeline entrypoint with two primary stages

**Chosen:** one orchestration entrypoint that exposes `create` and `tune` as the primary user-facing actions.

**Alternatives considered:**
- Keep separate skill-creator, optimizer, and benchmark tools — rejected because it preserves the current cognitive split and keeps lifecycle transitions implicit.
- Use one command with many fine-grained subcommands only — rejected because it exposes internal module boundaries instead of the workflow the user actually cares about.

**Rationale:** The specs require one lifecycle for canonical skill authoring. Two primary stages map cleanly to the real author journey: first produce a skill plus evals, then optimize and assess it. Internally, the pipeline can still call benchmark and tuning modules separately, but those become implementation details rather than product boundaries.

### Decision: Introduce a workflow state object for canonical skills

**Chosen:** represent each canonical skill in the pipeline through a single workflow-state abstraction that resolves the skill artifact, associated eval artifact, lifecycle status, run outputs, and promotion state.

**Alternatives considered:**
- Keep inferring paths independently in each script — rejected because current path inference is duplicated and makes resume/audit behavior fragile.
- Move all state into a global database first — rejected because it adds operational complexity before the workflow contract itself is stable.

**Rationale:** The new `skills` and `evals` deltas require the pipeline to consistently resolve canonical artifacts and retain enough state for resuming and auditing. A lightweight file-backed workflow state is sufficient for the canonical repository and fits existing artifact-oriented patterns better than introducing a service dependency.

### Decision: Separate pipeline orchestration from provider transport

**Chosen:** define a provider-neutral model transport interface and make stage code depend only on that interface.

**Alternatives considered:**
- Standardize on Copilot SDK only — rejected because the proposal explicitly targets Codex/Claude/Copilot interoperability and current duplication already shows the limitation of provider-specific plumbing.
- Let each module keep its own provider wrapper behind a similar method name — rejected because it keeps retries, auth, response parsing, and capability checks fragmented.

**Rationale:** Current code contains multiple Copilot wrappers in `skill-creator`, `benchmark`, and `tune`. The new transport layer removes duplication and makes provider choice a configuration concern. This also allows benchmarking and tuning to compare models fairly because the surrounding pipeline path remains constant.

### Decision: Keep benchmark as a lifecycle gate, not a separate product

**Chosen:** benchmark execution remains an explicit stage inside the `tune` lifecycle and produces independently inspectable results used for promotion decisions.

**Alternatives considered:**
- Fold benchmark fully into tuning score calculation with no separate identity — rejected because it weakens validation visibility.
- Keep benchmark as a completely separate user-facing tool — rejected because it forces authors to manually stitch together the workflow.

**Rationale:** The tuning delta requires benchmark to remain an explicit decision input, while the pipeline change requires users not to think in separate products. Treating benchmark as an internal lifecycle gate satisfies both: it remains visible in outputs and policy decisions without being a separate mental model.

### Decision: Keep local calibration out of the canonical authoring pipeline

**Chosen:** local calibration remains a downstream repo-specific adaptation workflow and is not part of canonical skill promotion.

**Alternatives considered:**
- Merge local calibration into `tune` by default — rejected because repo-local conventions and canonical skill quality are different concerns with different ownership.
- Defer local calibration entirely from the architecture — rejected because existing specs already recognize it as a necessary capability.

**Rationale:** Canonical skills should represent global, reusable review behavior. Local calibration overlays repository-specific preferences after that baseline exists. Keeping the boundary explicit avoids contaminating canonical promotion decisions with repo-specific signals.

### Decision: Add eval readiness validation before tuning

**Chosen:** the create stage must run an eval readiness check before the skill can be marked ready for tuning.

**Alternatives considered:**
- Trust generated evals and let tuning expose problems later — rejected because weak evals produce misleading optimization behavior and noisy benchmark results.
- Require manual review of every generated eval file — rejected because it slows down the happy path unnecessarily.

**Rationale:** The new eval requirements demand positive/negative coverage and explicit failure visibility. A lightweight readiness validator catches structurally weak datasets early without making human review mandatory for every iteration.

### Decision: Record explicit promotion outcomes

**Chosen:** every tune run ends in one of three explicit outcomes: promotable, gated for additional validation, or needs manual review.

**Alternatives considered:**
- Keep only raw logs and let users infer the result — rejected because the specs require explicit post-tuning visibility.
- Treat anything below target as silent failure — rejected because unresolved skills need durable follow-up and should integrate with `needs-review.md`.

**Rationale:** Current cascade behavior already distinguishes success from review-needed cases. Formalizing promotion outcomes lets the pipeline expose clear lifecycle status and use benchmark results, cascade thresholds, and policy checks consistently.

## Data Flow

### Create stage

1. The pipeline resolves the target canonical skill identity from user input or existing artifacts.
2. The authoring component drafts or refines `skills/<skill>/SKILL.md`.
3. The eval-generation component creates or updates `evals/<skill>.json`.
4. The eval readiness validator checks that the generated dataset is structurally usable for validation and tuning.
5. A quick validation pass runs against the linked skill/eval pair and writes report artifacts.
6. Workflow state is updated to show that the skill has linked evals and whether it is ready to enter tuning.

### Tune stage

1. The pipeline loads workflow state for the canonical skill and resolves the skill plus eval artifacts.
2. The tuning stage invokes the configured cascade sequence.
3. Each cascade stage uses the shared model transport, scoring, and mutation components to attempt improvement.
4. If a candidate clears tuning policy, the pipeline records the best candidate and may invoke benchmark validation.
5. Benchmark output is written as an inspectable artifact and fed into the promotion decision.
6. The final outcome is recorded as promotable, gated, or manual-review-required.
7. If manual review is required, the needs-review tracker is updated with the canonical skill identity and supporting artifacts.

### Provider flow

1. Pipeline stages construct provider-neutral completion requests.
2. The selected transport adapts the request to the configured provider.
3. Provider-specific auth, retries, and response parsing occur inside the transport layer only.
4. Stage logic receives normalized responses and remains unaware of provider session details.

## API Changes

No external API changes.

Internal interface changes are expected:

- a new pipeline-level CLI/entry module for `create` and `tune`
- a shared model transport interface replacing direct provider wrapper usage in stage code
- a shared workflow-state interface used by authoring, tuning, and benchmark stages

## Dependencies

No new mandatory external dependencies are required by the design.

The design assumes continued support for existing model transports already used by the repository, with Copilot SDK remaining the default. Additional provider adapters for Claude and Codex should plug into the shared transport layer rather than introduce new pipeline dependencies.

## Migration / Backwards Compatibility

This design is backward compatible at the artifact level:

- canonical skills remain in `skills/<skill>/SKILL.md`
- evals remain in `evals/<skill>.json`
- existing tuning and benchmark modules remain reusable as internal components
- `skills-tools/needs-review.md` remains the human-facing manual-review surface

Migration is primarily organizational:

- existing user-facing docs and tool boundaries will be reframed around the pipeline lifecycle
- duplicated provider wrappers will be migrated behind the shared transport interface
- existing scripts can remain temporarily available during transition, but the new pipeline entrypoint becomes the canonical workflow

No existing skill or eval data requires format migration for this change beyond adding workflow-state metadata alongside current artifacts.

## Testing Strategy

- **Unified skill authoring workflow**
  - integration tests for `create` stage orchestration across skill draft, eval generation, readiness validation, and artifact linkage

- **Skill workflow state association**
  - unit tests for artifact resolution and lifecycle state transitions
  - integration tests for resume/audit flows using existing skills and evals

- **Create-stage eval generation**
  - integration tests ensuring create produces a linked eval file for the target skill

- **Eval quality gate**
  - unit tests for readiness validation on missing negatives, missing positives, malformed assertions, and empty datasets

- **Unified tuning entry**
  - integration tests verifying that tuning runs through the pipeline entrypoint and still resolves the canonical skill identifier correctly

- **Provider-agnostic model interaction**
  - unit tests using fake transports to verify stage logic does not depend on provider-specific behavior
  - adapter contract tests for each supported provider implementation

- **Benchmark as lifecycle validation**
  - integration tests verifying benchmark artifacts are produced and promotion logic consumes them without hiding benchmark outputs

- **Promotion decision visibility**
  - integration tests covering promotable, gated, and needs-review outcomes
  - regression tests ensuring failed cascades still update `needs-review.md`

- **Local calibration boundary**
  - tests verifying calibration outputs remain separate from canonical promotion artifacts and do not alter canonical lifecycle state

## Edge Cases

- **Existing skill without evals**
  - `tune` must fail clearly and direct the workflow back to `create` or eval generation rather than guessing inputs.

- **Generated evals are structurally valid but weak**
  - readiness validation should mark them not ready for tuning and surface the reason explicitly.

- **Provider capability mismatch**
  - if a selected provider cannot satisfy a stage requirement, the pipeline should fail with a stage-level configuration error rather than silently degrading behavior.

- **Interrupted tuning runs**
  - workflow state and run artifacts must make it possible to distinguish an incomplete run from a completed but failed run.

- **Benchmark passes but tuning policy fails**
  - promotion must remain policy-driven; benchmark is a decision input, not the only signal.

- **Concurrent updates to manual review state**
  - the needs-review tracker should remain idempotent and preserve existing entries when multiple runs touch the queue.

- **Transition period with legacy scripts**
  - documentation and entrypoint behavior must make the pipeline the preferred path without breaking existing scripts that are still used internally.
