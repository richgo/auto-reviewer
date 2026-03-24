# skills Specification Delta

## ADDED Requirements

### Requirement: Skill Atomicity for Tuning and Scoring

The system SHALL treat each skill as the smallest independently tuneable and benchmarkable review unit.

#### Scenario: Skill-Scoped Tuning Targets

- GIVEN a tuning run is planned
- WHEN optimization targets are enumerated
- THEN targets SHALL be expressed as skill identifiers
- AND targets SHALL be expressed as skill identifiers only.

#### Scenario: Skill-Scoped Benchmark Reporting

- GIVEN benchmark execution over review capabilities
- WHEN skill/eval pairs are discovered and scored
- THEN each executable pair SHALL be keyed by skill identifier
- AND score outputs SHALL be reported at skill granularity.

### Requirement: Skill-Owned Review Guidance

The system SHALL store bug-class review guidance in skills as the canonical source for active review behavior.

#### Scenario: Migrated Guidance Availability

- GIVEN a bug class in the review coverage surface
- WHEN migration validation is performed
- THEN equivalent guidance SHALL exist in one or more skill artifacts
- AND active review behavior SHALL resolve through skill artifacts.

### Requirement: Skill-Level Coverage Preservation

The system SHALL preserve concern and platform coverage through the skill corpus.

#### Scenario: Concern and Platform Continuity

- GIVEN the set of concerns and platform-specific guidance supported before migration
- WHEN coverage is validated after migration
- THEN each concern SHALL be represented by at least one skill
- AND previously supported platform-specific guidance SHALL remain represented in skills.

### Requirement: Skill-Eval Ownership

The system SHALL associate eval datasets directly with skill identifiers.

#### Scenario: Eval Resolution by Skill

- GIVEN an eval case used by benchmark or tuning workflows
- WHEN the eval case is resolved for execution
- THEN it SHALL map to a skill identifier
- AND execution SHALL depend only on skill artifacts.

### Requirement: Skill-Level Security Reference Mapping

The system SHALL maintain security reference mappings at the skill layer.

#### Scenario: Security Reference Traceability

- GIVEN a security capability is reviewed for reference traceability
- WHEN references are inspected in the canonical review layer
- THEN relevant OWASP or equivalent security references SHALL be available through security skills
- AND reference completeness SHALL be satisfied through security skill artifacts.
