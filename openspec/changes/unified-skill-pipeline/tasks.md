# Tasks: Unified Skill Pipeline

## Phase 1: Shared Foundations

- [x] **1.1** Introduce shared provider transport interfaces
  Add a shared model transport module under `scripts/` for provider-neutral request/response handling, and refactor existing Copilot-specific wrappers in `scripts/tune/llm_client.py`, `scripts/benchmark/copilot_client.py`, and `skills-tools/skill-creator/scripts/copilot_sdk.py` to align behind it. Covers `tuning` spec requirement **Provider-Agnostic Model Interaction**.

- [ ] **1.2** Add canonical workflow-state support for skills
  Create a workflow-state layer that resolves a canonical skill, its linked eval file, and lifecycle metadata without changing the existing `skills/<skill>/SKILL.md` and `evals/<skill>.json` layout. Touch new pipeline/state files plus resolution logic used by `scripts/tune/` and authoring flows. Covers `skills` spec requirements **Unified Skill Authoring Workflow** and **Skill Workflow State Association**, plus `evals` **Eval File Lifecycle Ownership**.

- [ ] **1.3** Define promotion outcome records
  Add a shared outcome model for `promotable`, `gated`, and `needs_review` results, and integrate it with existing tuning history / `scripts/tune/needs_review.py` flows so unresolved candidates remain visible. Covers `tuning` spec requirement **Promotion Decision Visibility**.

## Phase 2: Create Stage

- [ ] **2.1** Build the pipeline `create` stage entrypoint
  Add a pipeline orchestration entry module that accepts a canonical skill target and coordinates draft/update flow using existing authoring helpers from `skills-tools/skill-creator/scripts/`. Touch the new pipeline entry module and minimal adapters around authoring scripts. Covers `skills` **Unified Skill Authoring Workflow**.

- [ ] **2.2** Wire create-stage eval generation
  Integrate eval creation/update into the `create` stage so every created or revised skill produces a linked `evals/<skill>.json` artifact. Touch create-stage orchestration plus eval generation/resolution helpers. Covers `evals` **Create-Stage Eval Generation** and **Eval File Lifecycle Ownership**.

- [ ] **2.3** Add eval readiness validation
  Implement readiness checks for generated evals, including explicit failure reporting for empty or unbalanced datasets before tuning can start. Touch new eval validation logic and create-stage workflow state updates. Covers `evals` **Eval Quality Gate for Authoring**.

- [ ] **2.4** Emit create-stage validation artifacts
  Reuse the existing quick eval/report path to produce a lightweight validation artifact from `create`, and record the readiness result in workflow state. Touch create-stage orchestration plus report-writing adapters in `skills-tools/skill-creator/scripts/run_loop.py` or adjacent helpers. Supports `skills` **Skill Workflow State Association** and `evals` lifecycle requirements.

## Phase 3: Tune Stage

- [ ] **3.1** Build the pipeline `tune` stage entrypoint
  Extend the pipeline orchestration entry module with a `tune` stage that resolves the canonical skill and eval artifacts from workflow state and fails clearly when required inputs are missing. Covers `tuning` **Unified Tuning Entry** and edge case handling from the design.

- [ ] **3.2** Refactor autoresearch and cascade behind pipeline contracts
  Adapt `scripts/tune/autoresearch.py`, `scripts/tune/cascade.py`, and related modules to use the shared workflow state and provider transport interfaces rather than direct provider/session assumptions. Covers `tuning` **Unified Tuning Entry** and **Provider-Agnostic Model Interaction**.

- [ ] **3.3** Integrate benchmark as a tune-stage validation gate
  Update tune-stage orchestration so benchmark execution can run as an explicit validation step and feed promotion decisions while preserving independently inspectable benchmark artifacts. Touch `scripts/benchmark/runner.py`, tune orchestration, and outcome recording. Covers `tuning` **Benchmark as Lifecycle Validation**.

- [ ] **3.4** Preserve the local-calibration boundary
  Update documentation and orchestration boundaries so `local-calibration` remains outside canonical create/tune promotion flow and its outputs remain distinguishable from canonical skill artifacts. Touch pipeline docs and any tuning/orchestration boundary code that currently blurs this separation. Covers `tuning` **Local Calibration**.

## Phase 4: Documentation and Migration

- [ ] **4.1** Update skill authoring documentation to pipeline-first language
  Revise `skills-tools/creating-skills.md` and related human-facing docs so they point authors to the unified lifecycle rather than separate creator/optimizer/benchmark products. Covers `skills` **Unified Skill Authoring Workflow** and the design migration plan.

- [ ] **4.2** Add transition guidance for legacy entrypoints
  Document which existing scripts remain supported as internal building blocks during migration and which new pipeline entrypoint is canonical. Touch docs near `skills-tools/` and any README/help text associated with the new entry module. Supports backward compatibility decisions in the design.

## Phase 5: Testing & Verification

- [ ] **5.1** Write unit tests for provider transport and workflow state
  Add tests covering provider-neutral request/response behavior, artifact resolution, lifecycle state transitions, and explicit failure on missing inputs. Reference `skills` **Skill Artifact Resolution** and `tuning` **Shared Model Contract** scenarios.

- [ ] **5.2** Write unit tests for eval readiness validation and promotion outcomes
  Add tests for missing positives, missing negatives, malformed evals, not-ready states, and explicit `promotable` / `gated` / `needs_review` outcome recording. Reference `evals` **Eval Readiness Check** and `tuning` **Post-Tuning Outcome** scenarios.

- [ ] **5.3** Write integration tests for the `create` stage
  Add integration coverage showing that `create` produces or updates a canonical skill/eval pair, emits validation artifacts, and records workflow state. Reference `skills` **Authoring Lifecycle Entry** and `evals` **Eval Creation During Skill Authoring** scenarios.

- [ ] **5.4** Write integration tests for the `tune` stage
  Add integration coverage showing that `tune` resolves canonical artifacts, runs the cascade through the shared transport layer, invokes benchmark as a validation stage, and updates manual-review tracking when needed. Reference `tuning` **Tuning Stage Invocation**, **Benchmark as Lifecycle Validation**, and **Post-Tuning Outcome** scenarios.

- [ ] **5.5** Write boundary tests for local calibration separation
  Add regression tests ensuring local calibration outputs do not overwrite canonical workflow state or promotion artifacts. Reference `tuning` **Calibration Boundary**.

- [ ] **5.6** Manual verification
  Manually verify an end-to-end flow: run `create` for a new or sample skill, confirm linked eval generation and readiness reporting, then run `tune`, confirm benchmark visibility, and verify that failed runs update `skills-tools/needs-review.md` while calibration remains separate.
