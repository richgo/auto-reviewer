# Tasks: Flatten Skills to Claude Structure

## Phase 1: Canonical Skill Identity and Layout

- [x] **1.1** Build canonical skill inventory and flattened-name map  
  Enumerate active skills and nested review-task-derived entries, derive canonical flattened identifiers, and produce a deterministic inventory used by downstream migration checks.  
  **Files:** `skills/**`, `scripts/skills/migration_map.py` (or equivalent inventory surface)  
  **Done when:** Every active source resolves to one proposed canonical identifier with no unmapped artifacts.  
  **Spec coverage:** `skills` / Canonical Skill Folder Contract, Flattened Name Resolution.

- [x] **1.2** Define and apply canonical folder contract  
  Transition active skill placement to one-folder-per-skill with `SKILL.md` entry ownership in the planned target structure.  
  **Files:** `skills/**`  
  **Done when:** Active skill identity can be validated solely by `<skill-name>/SKILL.md`.  
  **Spec coverage:** `skills` / Canonical Skill Folder Contract, Guidance Resolution Through Canonical Skills.

- [x] **1.3** Merge duplicate flattened targets into single canonical skills  
  For identifiers with multiple source artifacts, consolidate content into one canonical `SKILL.md` and retire competing active definitions.  
  **Files:** `skills/**`  
  **Done when:** Each canonical identifier has exactly one active `SKILL.md`.  
  **Spec coverage:** `skills` / Canonical Duplicate Merge, Front Matter Consolidation.

- [x] **1.4** Resolve naming divergences and record canonical ownership  
  Resolve cases like `data` lineage vs `data-integrity` ownership using explicit canonical naming decisions in active contracts.  
  **Files:** `skills/**`, `openspec/changes/flatten-skills-claude-structure/specs/**`  
  **Done when:** Divergent names no longer create ambiguous active ownership.  
  **Spec coverage:** `skills` / Flattened Name Resolution, Canonical Duplicate Merge.

## Phase 2: Contract Alignment and Strict Cutover

- [x] **2.1** Update composition policy and validator assumptions to canonical identity  
  Align dependency selection/validation to canonical foldered skills and remove acceptance of legacy alias paths.  
  **Files:** `scripts/compose/policy.yaml`, `scripts/compose/validator.py`, `scripts/compose/*.py`, `agents/composer/agent.md`  
  **Done when:** Legacy skill references fail validation and canonical identities pass.  
  **Spec coverage:** `agent-composition` / Canonical Dependency Resolution, Legacy Reference Rejection.

- [x] **2.2** Update benchmark/tuning discovery to canonical folder discovery  
  Align skill discovery contracts to resolve canonical `SKILL.md` folders only.  
  **Files:** `scripts/benchmark/runner.py`, `scripts/tune/orchestrator.py`  
  **Done when:** Discovery no longer depends on category-local `*.md` skill files.  
  **Spec coverage:** `agent-composition` / Canonical Skill Discovery Contract; `review-tasks` / Runtime Independence from Review-Task Trees.

- [x] **2.3** Align skill mapping outputs and lineage references  
  Update migration mapping outputs to reference canonical flattened skill identities and non-normative historical lineage.  
  **Files:** `scripts/skills/migration_map.py`, related artifacts/tests  
  **Done when:** Mapping output references canonical active skill identities without requiring nested runtime trees.  
  **Spec coverage:** `review-tasks` / Nested-to-Flat Lineage Clarity; `skills` / Guidance Resolution Through Canonical Skills.

- [x] **2.4** Update docs/spec language for strict no-legacy active behavior  
  Ensure README and OpenSpec surfaces describe canonical foldered skills as exclusive active contract.  
  **Files:** `README.md`, `openspec/specs/review-tasks/spec.md`, relevant change docs  
  **Done when:** No active contract text implies legacy skill-path support.  
  **Spec coverage:** `review-tasks` / Historical Inspection Boundaries; `agent-composition` / Legacy Reference Rejection.

## Phase 3: Conflict Reporting, Tests, and Verification

- [x] **3.1** Add manual conflict error reporting for non-mergeable duplicates  
  Implement conflict diagnostics that report unresolved canonicalization issues with skill identifier context.  
  **Files:** validation/reporting surfaces under `scripts/skills/` and/or `scripts/compose/`  
  **Done when:** Non-mergeable conflicts are emitted as actionable manual-fix errors.  
  **Spec coverage:** `skills` / Non-Mergeable Content Conflict.

- [x] **3.2** Add/adjust tests for canonical skill structure and flattening rules  
  Add unit/contract tests covering folder contract, flattened naming, duplicate canonical ownership, and front matter ownership.  
  **Files:** `scripts/tests/skills/**`, `scripts/tests/compose/**`  
  **Done when:** Tests enforce one canonical `SKILL.md` per active skill identifier.  
  **Spec coverage:** `skills` scenarios in full.

- [x] **3.3** Add tests for strict legacy rejection and canonical discovery  
  Add tests that ensure legacy dependency references are rejected and compose/tune/benchmark discovery uses canonical folders only.  
  **Files:** `scripts/tests/compose/**`, `scripts/tests/tune/**`, `scripts/tests/benchmark/**`  
  **Done when:** Legacy references fail deterministically with explicit validation errors.  
  **Spec coverage:** `agent-composition` scenarios in full.

- [x] **3.4** Manual verification  
  Validate end-to-end behavior: canonical discovery succeeds, legacy references fail, duplicate merges are singular, and unresolved conflicts are listed for manual fix.  
  **Files/commands:** repository validation + existing test commands  
  **Done when:** All spec scenarios are demonstrated by automated tests or manual checks with clear evidence.
