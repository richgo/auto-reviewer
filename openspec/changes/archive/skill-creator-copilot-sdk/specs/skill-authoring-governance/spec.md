# skill-authoring-governance Specification Delta

## ADDED Requirements

### Requirement: Upstream Skill-Creator Provenance Contract

The system SHALL maintain explicit provenance when reusing upstream `skill-creator` guidance.

#### Scenario: Traceable Upstream Baseline

- GIVEN repository guidance references Anthropic `skills/skill-creator` content
- WHEN contributors inspect the local skill-creator capability documentation
- THEN the documentation SHALL identify the upstream source and local ownership boundary
- AND the repository SHALL distinguish baseline upstream content from local adaptations

### Requirement: Controlled Upstream Refresh Workflow

The system SHALL define a controlled process for evaluating and applying upstream `skill-creator` changes.

#### Scenario: Upstream Guidance Changes

- GIVEN upstream `skill-creator` guidance has changed
- WHEN maintainers evaluate whether to update local guidance
- THEN the update decision SHALL be recorded as an explicit repository change
- AND local deviations from upstream SHALL remain intentional and documented

### Requirement: Reuse Boundary Across Authoring Surfaces

The system SHALL keep skill-authoring guidance consistent across all affected repository surfaces.

#### Scenario: Skill Authoring Contract Review

- GIVEN the repository defines skill-authoring behavior in multiple documents
- WHEN maintainers review capability docs and README guidance
- THEN all normative guidance SHALL align with the same skill-creator contract
- AND conflicting parallel authoring contracts SHALL NOT be introduced

