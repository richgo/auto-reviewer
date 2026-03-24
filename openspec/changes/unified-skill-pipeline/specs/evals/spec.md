# evals Specification Delta

## ADDED Requirements

### Requirement: Create-Stage Eval Generation

The system SHALL support eval generation as part of the initial canonical skill authoring workflow.

#### Scenario: Eval Creation During Skill Authoring

- GIVEN a canonical skill is being created or substantially revised
- WHEN the create stage completes
- THEN the system SHALL produce or update an eval dataset associated with that skill
- AND the resulting eval dataset SHALL remain directly keyed to the canonical skill identifier

### Requirement: Eval Quality Gate for Authoring

The system SHALL validate generated eval datasets for minimum usefulness before they are used for tuning or promotion decisions.

#### Scenario: Eval Readiness Check

- GIVEN an eval dataset is produced or updated for a canonical skill
- WHEN the dataset is marked ready for tuning
- THEN the system SHALL verify that the dataset contains positive and negative coverage suitable for scoring
- AND the system SHALL make eval readiness failures explicit instead of silently allowing weak datasets into the tuning pipeline

## MODIFIED Requirements

### Requirement: Eval Infrastructure Format

The system SHALL define eval test cases in structured JSON files for automated validation and SHALL treat those files as first-class artifacts of canonical skill authoring.

(Previously: The system SHALL define eval test cases in structured JSON files for automated validation.)

#### Scenario: Eval File Lifecycle Ownership

- GIVEN skills need automated testing
- WHEN an eval file is created, updated, or resolved by the workflow
- THEN it SHALL exist as a canonical artifact associated with a skill identifier
- AND the authoring lifecycle SHALL be able to use that artifact for validation, tuning, and benchmark stages

