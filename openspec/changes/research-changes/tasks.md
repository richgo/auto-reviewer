# Tasks: Research Changes

## Phase 1: Primitive Flattening and Skill Canonicalization

- [x] **1.1** Create review-task to skill migration map
  Build a deterministic mapping inventory from `review-tasks/**/*.md` to owning skill artifacts in `skills/` (including concern/platform ownership and security reference lineage). Produce migration notes in this change folder as implementation artifacts. (Specs: `skills` Migrated Guidance Availability, Concern and Platform Continuity, Security Reference Traceability; Design: Migrate Review-Task Guidance into Skills)

- [x] **1.2** Migrate review guidance from `review-tasks/` into skill artifacts
  Consolidate task-level guidance into canonical skill files (and skill-local references where needed) so active review behavior resolves through `skills/` only. Keep coverage complete across concerns/platforms and preserve security reference traceability. (Specs: `skills` Skill-Owned Review Guidance, Skill-Level Coverage Preservation, Skill-Level Security Reference Mapping)

- [ ] **1.3** Align eval ownership to skill-linked source of truth
  Update eval/documentation surfaces so benchmark and tuning inputs are explicitly skill-mapped and do not depend on standalone task-local eval snippets. Touch `evals/` metadata and relevant docs/contracts only as needed for clarity. (Specs: `skills` Skill-Eval Ownership; `review-tasks` Eval Source of Truth; Design Data Flow steps 2-4)

- [ ] **1.4** Retire active review-task architecture role
  Transition `review-tasks/` from active runtime architecture to migrated/historical status, including repository structure and explanatory docs. Ensure active execution/tuning/benchmark descriptions no longer require this directory. (Specs: `review-tasks` Transitional Task Usage, Taxonomy Resolution in Active Architecture; Design Migration/Backwards Compatibility)

## Phase 2: Agent Composition and Contract Alignment

- [ ] **2.1** Update agent contracts to explicit skill-group semantics
  Revise agent-facing contracts in `agents/composer/agent.md`, `agents/adversarial/agent.md`, and related orchestration docs to make skill grouping/delegation explicit and prohibit alternate atomic primitives. (Specs: `agent-composition` Agent Composition Declaration, Subagent Delegation)

- [ ] **2.2** Align composition policy and docs to skill-only dependencies
  Confirm `scripts/compose/policy.yaml` and composition-facing docs/contracts are strictly skill-path based and contain no dependency expectations on standalone review-task artifacts. (Specs: `agent-composition` Signal-Driven Composition; Design: Keep Existing Runtime Entry Points)

- [ ] **2.3** Normalize pipeline and architecture language across docs/specs
  Update `README.md`, `openspec/specs/review-tasks/spec.md`, and relevant active OpenSpec phase docs so architecture language consistently presents skills as atomic and agents as wrappers. Preserve historical context with explicit non-normative labeling where needed. (Specs: `review-tasks` modified/removed requirements + `skills` Skill Atomicity; Design: Legacy references handling)

- [ ] **2.4** Add skill-attribution contract language for agent outputs
  Update orchestration/output contract docs so review outputs are attributable to participating skills and delegation remains traceable at skill level. (Specs: `agent-composition` Review Output Attribution; Design Data Flow step 7)

## Phase 3: Testing & Verification

- [ ] **3.1** Write unit/contract tests for skill-atomic tuning and benchmark discovery
  Add or update tests under `scripts/tests/tune/` and `scripts/tests/benchmark/` to verify planning/discovery remains skill-scoped and does not require review-task identifiers. (Covers specs: `skills` Skill-Scoped Tuning Targets, Skill-Scoped Benchmark Reporting, Eval Resolution by Skill; `review-tasks` Transitional Task Usage)

- [ ] **3.2** Write integration tests for composition and agent traceability
  Add/extend tests under `scripts/tests/compose/` plus contract tests for `agents/*` docs to verify skill-path dependency selection, subagent delegation semantics, and skill-attributable output routing language remain intact. (Covers specs: `agent-composition` Signal-Driven Composition, Subagent Delegation, Review Output Attribution)

- [ ] **3.3** Write migration integrity and coverage regression checks
  Add verification tests/fixtures that assert migrated guidance completeness from prior review-task corpus, including concern/platform continuity and security reference availability in skills. (Covers specs: `skills` Migrated Guidance Availability, Concern and Platform Continuity, Security Reference Traceability; `review-tasks` Taxonomy Resolution in Active Architecture)

- [ ] **3.4** Manual verification
  Perform end-to-end verification: (1) inspect docs/specs for skill-first consistency, (2) run tune/benchmark planning to confirm skill-only targeting, (3) run compose path checks for skill-only dependencies, and (4) confirm no active runtime contract requires standalone `review-tasks/`.
