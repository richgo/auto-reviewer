# Tasks: Skill Creator Copilot SDK Reuse

## Phase 1: OpenSpec Contract Foundation

- [x] **1.1** Finalize proposal scope and risk framing  
  Update `openspec/changes/skill-creator-copilot-sdk/proposal.md` to ensure intent/scope explicitly cover upstream `skill-creator` reuse boundaries and Copilot SDK-first runtime alignment.  
  **Completion:** Proposal text clearly separates in-scope/out-of-scope and identifies affected repository surfaces.  
  **Specs:** `skill-authoring-governance` (all scenarios), `copilot-sdk-runtime-alignment` (all scenarios).

- [x] **1.2** Add skill-authoring governance capability delta  
  Create/confirm `openspec/changes/skill-creator-copilot-sdk/specs/skill-authoring-governance/spec.md` with SHALL requirements for provenance, upstream refresh control, and cross-surface reuse consistency.  
  **Completion:** Spec includes Given/When/Then scenarios for each requirement.  
  **Specs:** `skill-authoring-governance` / Traceable Upstream Baseline, Upstream Guidance Changes, Skill Authoring Contract Review.

- [x] **1.3** Add Copilot runtime alignment capability delta  
  Create/confirm `openspec/changes/skill-creator-copilot-sdk/specs/copilot-sdk-runtime-alignment/spec.md` with SHALL requirements for Copilot SDK default guidance, runtime example consistency, and historical Claude reference labeling.  
  **Completion:** Spec includes Given/When/Then scenarios for each requirement.  
  **Specs:** `copilot-sdk-runtime-alignment` / Normative Runtime Guidance, Example Command Review, Mixed Historical Documentation.

## Phase 2: Design and Traceability

- [x] **2.1** Document technical decisions and alternatives  
  Update `openspec/changes/skill-creator-copilot-sdk/design.md` with explicit decisions on baseline-and-adapt reuse model, default-runtime policy, and historical-reference handling.  
  **Completion:** Each decision includes alternatives considered and rationale.  
  **Specs:** `skill-authoring-governance` (all scenarios), `copilot-sdk-runtime-alignment` (all scenarios).

- [x] **2.2** Map data flow and component impact  
  Update `design.md` architecture/data-flow sections to show how upstream refresh and runtime-language normalization propagate across `README.md`, `skills/tuning/*.md`, and `agents/*/agent.md`.  
  **Completion:** Affected components and flow steps are explicit and non-contradictory with specs.  
  **Specs:** `skill-authoring-governance` / Skill Authoring Contract Review; `copilot-sdk-runtime-alignment` / Normative Runtime Guidance.

- [ ] **2.3** Map tests to spec scenarios  
  Update `design.md` testing strategy so every scenario in both spec files has a corresponding verification approach.  
  **Completion:** Scenario-to-test mapping is complete and reviewable.  
  **Specs:** all scenarios in both capability deltas.

## Phase 3: Implementation Planning Checklist (No Code Changes)

- [ ] **3.1** Plan provenance labeling updates in tuning docs  
  Prepare documentation update checklist for `skills/tuning/skill-optimizer.md`, `skills/tuning/benchmark-runner.md`, and `skills/tuning/local-calibration.md` to reflect upstream provenance boundaries and runtime-default language.  
  **Completion:** Checklist identifies exact sections requiring provenance/default-runtime edits.  
  **Specs:** `skill-authoring-governance` / Traceable Upstream Baseline; `copilot-sdk-runtime-alignment` / Normative Runtime Guidance.

- [ ] **3.2** Plan runtime-default normalization in top-level docs  
  Prepare checklist for `README.md` and relevant agent docs to ensure Copilot SDK-first defaults and labeled provider alternatives.  
  **Completion:** Checklist enumerates files and acceptance conditions for consistency review.  
  **Specs:** `copilot-sdk-runtime-alignment` / Example Command Review, Mixed Historical Documentation.

- [ ] **3.3** Plan historical reference de-emphasis pass  
  Prepare audit checklist for identifying unlabeled Claude CLI references in normative sections and marking them historical/non-default where retained.  
  **Completion:** Audit checklist includes detection criteria and pass/fail conditions.  
  **Specs:** `copilot-sdk-runtime-alignment` / Mixed Historical Documentation.

## Phase 4: Coherence Verification

- [ ] **4.1** Verify proposal-to-spec coverage  
  Confirm each scope item in `proposal.md` maps to one or more requirements in the two spec deltas.  
  **Completion:** Written trace matrix (in review notes/PR description) shows complete mapping.  
  **Specs:** all scenarios in both capability deltas.

- [ ] **4.2** Verify spec-to-design coverage  
  Confirm each spec requirement has a corresponding design decision, flow step, or testing strategy entry.  
  **Completion:** No requirement remains without design coverage.  
  **Specs:** all scenarios in both capability deltas.

- [ ] **4.3** Verify spec-to-task coverage and ordering  
  Confirm each spec scenario is covered by at least one task and tasks are ordered so later work does not unblock earlier dependencies.  
  **Completion:** Task list is dependency-safe and execution-ready.  
  **Specs:** all scenarios in both capability deltas.
