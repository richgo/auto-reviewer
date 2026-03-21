# Tasks: Phase 4 Composer Agent

## Phase 1: Agent Entry and Composition Core

- [x] **1.1** Create composer agent entry instructions  
  Add `agents/composer/agent.md` (or repo-equivalent agent location) with compose and compose-update command flow, input/output contract, and managed-manifest boundaries. Ensure generated output targets `apm.yml` and references policy-constrained behavior. (Specs: composer-agent Agent-Driven Compose Entry scenario)

- [x] **1.2** Add declarative composition policy file  
  Create `scripts/compose/policy.yaml` mapping repository signals to core/concern/language/output skill paths, including fallback baseline entries for weak detection. Keep policy data-only and reviewable. (Specs: composer-manifest Repository-Aware Manifest Composition + composer-agent Safety Fallback scenarios; Design: Declarative Signal-to-Skill Policy)

- [x] **1.3** Implement repository signal detection module  
  Add `scripts/compose/detector.py` to scan root and subdirectories for language/platform/build/CI hints and return normalized capabilities suitable for policy resolution. Ensure monorepo union detection is supported. (Specs: composer-manifest Generate Manifest + Monorepo Union scenarios)

- [x] **1.4** Implement dependency selection and deterministic ordering  
  Add `scripts/compose/selector.py` to resolve detected capabilities through `policy.yaml`, include mandatory core skills, dedupe, and sort composer-managed dependencies deterministically. (Specs: composer-manifest Repository-Aware Manifest Composition + Deterministic Dependency Ordering scenarios)

## Phase 2: Validation, Merge, and APM Compatibility

- [x] **2.1** Implement reference strategy resolution  
  Add `scripts/compose/versioning.py` (or equivalent helper) to apply default stable refs and explicit override strategies (`tag|sha|branch|none`) to generated dependencies with consistent APM notation. (Specs: composer-manifest Version Pin Strategy scenarios; apm-integration Ref and Lockfile Compatibility scenario)

- [x] **2.2** Implement manifest validator with fail-closed behavior  
  Add `scripts/compose/validator.py` to validate dependency path existence, ref syntax, and manifest shape before writes. Return explicit errors and block partial output on invalid generation. (Specs: composer-manifest Validation Before Persist + composer-agent Policy-Constrained Agent Output scenarios)

- [x] **2.3** Implement scoped update merge for `apm.yml`  
  Add `scripts/compose/merge.py` to update only composer-managed auto-reviewer entries while preserving user-managed config and non-auto-reviewer dependencies. Support generate and update modes. (Specs: composer-manifest Update Mode with Scoped Merge + composer-agent Compositional Re-run Workflow scenarios)

- [x] **2.4** Wire compose orchestrator and manifest writer  
  Add `scripts/compose/composer.py` to run detect → select → version → validate → merge/write, emit stack summary metadata, and set compilation defaults for multi-runtime repositories. (Specs: composer-manifest all scenarios; apm-integration Install and Compile Readiness + Multi-Runtime Compilation Defaults scenarios)

- [x] **2.5** Update repository docs for compose lifecycle  
  Update `README.md` and relevant usage docs to describe compose generation, compose-update behavior, pin overrides, and expected `apm install` / `apm compile` flow. (Specs: composer-agent Agent-Driven Compose Entry + Compositional Re-run Workflow; apm-integration readiness scenarios)

## Phase 3: Testing & Verification

- [x] **3.1** Write unit tests for detector/selector/versioning/validator  
  Add tests under `scripts/tests/compose/` for signal detection (including monorepo unions), deterministic dependency ordering, default/override pin behavior, and fail-closed validation on invalid dependency/ref/shape. (Covers composer-manifest Generate Manifest, Monorepo Union, Deterministic Ordering, Version Pin, Validation scenarios)

- [x] **3.2** Write integration tests for compose generate/update flow  
  Add fixture-based integration tests that run compose end-to-end to create/update `apm.yml`, preserve non-managed sections, and verify fallback baseline behavior when detection signals are weak. (Covers composer-agent Compose Entry, Safety Fallback, Compositional Re-run; composer-manifest Scoped Merge scenario)

- [x] **3.3** Write APM compatibility verification tests  
  Add tests/assertions for produced manifest compatibility expectations: parseable dependency notation, multi-runtime compilation defaults present when applicable, and stable ref/lock intent across repeated runs. (Covers apm-integration Install and Compile Readiness, Multi-Runtime Compilation Defaults, Ref and Lockfile Compatibility scenarios)

- [x] **3.4** Manual verification  
  Manually run compose on (a) single-stack repo fixture and (b) polyglot/monorepo fixture; verify generated/updated `apm.yml` diffs are deterministic, preserved sections remain intact, invalid generation is rejected with explicit errors, and resulting manifest is ready for `apm install` and `apm compile`.
