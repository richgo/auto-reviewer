# tuning Specification Delta

## ADDED Requirements

### Requirement: Unified Tuning Entry

The system SHALL expose tuning as a primary stage of the canonical skill authoring pipeline.

#### Scenario: Tuning Stage Invocation

- GIVEN a canonical skill and associated eval dataset are available
- WHEN the user starts tuning for that skill
- THEN the system SHALL run tuning through the pipeline lifecycle rather than requiring separate user-facing optimizer and benchmark products
- AND tuning outcomes SHALL be attributable to the canonical skill identifier

### Requirement: Provider-Agnostic Model Interaction

The system SHALL define model interaction for authoring, tuning, and benchmark execution through a provider-agnostic interface.

#### Scenario: Shared Model Contract

- GIVEN pipeline stages need model completions
- WHEN a stage requests model interaction
- THEN the stage SHALL depend on a provider-neutral model contract rather than provider-specific session logic
- AND the contract SHALL support multiple providers without changing the stage-level workflow requirements

### Requirement: Promotion Decision Visibility

The system SHALL make promotion and manual-review outcomes explicit after tuning completes.

#### Scenario: Post-Tuning Outcome

- GIVEN a tuning run has completed for a canonical skill
- WHEN the pipeline evaluates the outcome against configured acceptance policy
- THEN the system SHALL record whether the tuned candidate is promotable, requires additional validation, or requires manual review
- AND unresolved candidates SHALL remain visible for follow-up instead of being silently discarded

## MODIFIED Requirements

### Requirement: Benchmark Runner

The system SHALL treat benchmark execution as a validation stage within the tuning lifecycle while preserving benchmark metrics as an explicit decision input.

(Previously: The system SHALL implement a benchmark-runner skill for automated skill testing.)

#### Scenario: Benchmark as Lifecycle Validation

- GIVEN skills need performance measurement
- WHEN benchmark execution is invoked during or after tuning
- THEN the system SHALL use benchmark results as an explicit validation input for lifecycle decisions
- AND benchmark execution SHALL remain independently inspectable even when invoked as part of the larger tuning pipeline

### Requirement: Local Calibration

The system SHALL preserve local calibration as a repo-specific adaptation capability that is separate from canonical skill authoring and promotion.

(Previously: The system SHALL implement a local-calibration skill for repo-specific tuning.)

#### Scenario: Calibration Boundary

- GIVEN a canonical skill has completed global authoring or tuning stages
- WHEN a repository applies local calibration
- THEN the calibration workflow SHALL adapt the skill for repo-specific conventions without redefining the canonical global authoring lifecycle
- AND calibration outputs SHALL remain distinguishable from canonical skill artifacts

