# Review Tasks Specification

## Requirement: Transitional Migration Inputs Only

The system SHALL treat review-task artifacts as historical migration inputs and not as active runtime units.

### Scenario: Runtime Independence

- GIVEN benchmark, tuning, or composition workflows execute
- WHEN runtime inputs are resolved
- THEN execution SHALL use skills and skill-linked eval datasets
- AND execution SHALL NOT require standalone review-task files.

## Requirement: Historical Taxonomy Context

The system SHALL keep any retained review-task taxonomy as historical, non-normative context only.

### Scenario: Non-Normative Labeling

- GIVEN archived review-task artifacts are present for audit
- WHEN users inspect repository documentation or contracts
- THEN those artifacts SHALL be clearly labeled historical/non-normative
- AND active coverage guarantees SHALL be defined at the skill layer.

## Requirement: Skill-Owned Eval Source

The system SHALL define skill-linked eval datasets as the executable source of truth.

### Scenario: Skill-Eval Resolution

- GIVEN an eval case is selected for benchmark or tuning
- WHEN the evaluator resolves execution inputs
- THEN the eval case SHALL map to a skill identifier
- AND task-local eval snippets SHALL not be required for execution.

