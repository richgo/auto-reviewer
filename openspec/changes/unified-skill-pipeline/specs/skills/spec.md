# skills Specification Delta

## ADDED Requirements

### Requirement: Unified Skill Authoring Workflow

The system SHALL present canonical skill authoring as one lifecycle that begins with skill creation and eval generation, then proceeds to tuning and promotion assessment.

#### Scenario: Authoring Lifecycle Entry

- GIVEN a user wants to add or improve a canonical skill
- WHEN the authoring workflow is initiated
- THEN the system SHALL treat skill drafting, eval association, and tuning preparation as stages of one workflow
- AND the workflow SHALL not require the user to manually compose separate end-user tools to advance between those stages

### Requirement: Skill Workflow State Association

The system SHALL maintain workflow state that associates each canonical skill with its authoring artifacts and lifecycle status.

#### Scenario: Skill Artifact Resolution

- GIVEN a canonical skill participates in the authoring pipeline
- WHEN the workflow resolves the skill for evaluation or tuning
- THEN the system SHALL be able to determine the canonical skill artifact and its associated eval dataset
- AND the system SHALL preserve enough workflow state to resume or audit the skill's lifecycle progression

## MODIFIED Requirements

### Requirement: Tuning Skills

The system SHALL define tuning-oriented capabilities as stages within the canonical skill authoring lifecycle, while preserving local calibration as a distinct repo-specific adaptation capability.

(Previously: The system SHALL enable continuous improvement via autoresearch-based tuning.)

#### Scenario: Lifecycle-Oriented Tuning Components

- GIVEN skills need optimization over time
- WHEN authoring and tuning capabilities are described
- THEN benchmark execution and prompt optimization SHALL be treated as lifecycle stages operating on canonical skills
- AND local calibration SHALL remain distinct from canonical skill authoring because it adapts behavior to repository-specific conventions

