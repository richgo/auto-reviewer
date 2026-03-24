# skills Specification Delta

## MODIFIED Requirements

### Requirement: Skill Format

The system SHALL define each active skill as a folder whose name is the canonical skill identifier and whose entry file is `SKILL.md`.

(Previously: skills were primarily represented as single markdown files under grouped directories.)

#### Scenario: Canonical Skill Folder Contract

- GIVEN a skill is part of the active corpus
- WHEN its on-disk structure is validated
- THEN the skill SHALL exist in a folder named exactly for that skill identifier
- AND the folder SHALL include `SKILL.md` as the canonical entry file
- AND active runtime discovery SHALL resolve through this folder contract.

### Requirement: Skill Naming Convention

The system SHALL use flattened, explicit skill identifiers for nested lineage and enforce one canonical identifier per active skill.

(Previously: naming requirements focused on file naming patterns and category-local paths.)

#### Scenario: Flattened Name Resolution

- GIVEN a nested skill lineage exists (for example `api-design/mobile`)
- WHEN canonical identifiers are derived
- THEN the active skill identifier SHALL be flattened to an explicit name preserving lineage semantics (for example `api-design-mobile`)
- AND nested folder hierarchy SHALL not be required for active skill identity.

#### Scenario: Canonical Duplicate Merge

- GIVEN multiple source artifacts resolve to the same flattened active skill identifier
- WHEN canonicalization is validated
- THEN those artifacts SHALL be represented by one active skill folder and one canonical `SKILL.md`
- AND active contracts SHALL treat that canonical artifact as the sole source of truth.

### Requirement: Skill-Owned Review Guidance

The system SHALL keep active review guidance in canonical skill folders and remove active dependence on legacy file-shaped skill representations.

(Previously: guidance ownership was skill-centric but did not require folder-based canonicalization.)

#### Scenario: Guidance Resolution Through Canonical Skills

- GIVEN review execution resolves guidance for a capability
- WHEN active sources are loaded
- THEN guidance SHALL be resolved from canonical skill folders
- AND active resolution SHALL not require legacy file-based skill placement.

## ADDED Requirements

### Requirement: Canonical Skill Front Matter Ownership

The system SHALL maintain one canonical front matter block per active skill, owned by the canonical `SKILL.md`.

#### Scenario: Front Matter Consolidation

- GIVEN multiple source artifacts contribute to one canonical skill identifier
- WHEN metadata ownership is validated
- THEN the canonical `SKILL.md` SHALL contain the authoritative front matter for that skill
- AND active contracts SHALL not rely on competing front matter definitions outside the canonical folder.

### Requirement: Manual Conflict Error Reporting

The system SHALL make non-mergeable canonicalization conflicts explicit for manual remediation.

#### Scenario: Non-Mergeable Content Conflict

- GIVEN source artifacts targeting one canonical skill cannot be safely unified
- WHEN canonicalization checks are performed
- THEN each conflict SHALL be reported as a manual-fix error with impacted skill identifier context
- AND the conflict SHALL remain visible until manually resolved.
