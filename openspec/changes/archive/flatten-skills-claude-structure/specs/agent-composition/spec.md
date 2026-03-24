# agent-composition Specification Delta

## MODIFIED Requirements

### Requirement: Composition Policy Uses Skill Dependencies

The system SHALL resolve composition dependencies to canonical skill-folder identities and SHALL NOT accept legacy path aliases.

(Previously: composition policy required skill dependencies but did not define canonical folder identity or strict no-legacy behavior.)

#### Scenario: Canonical Dependency Resolution

- GIVEN repository signals are detected for composition
- WHEN dependencies are selected and validated
- THEN selected dependencies SHALL resolve to canonical skill folder identities
- AND legacy or alias dependency forms SHALL be rejected.

### Requirement: Agent Output Traceability to Skills

The system SHALL attribute outputs to canonical skill identifiers.

(Previously: output attribution to skills was required without explicit canonical identifier constraints.)

#### Scenario: Canonical Skill Attribution

- GIVEN a review output produced by an agent flow
- WHEN output attribution context is inspected
- THEN attribution SHALL reference canonical skill identifiers
- AND attribution SHALL remain stable across flattened path migration.

## ADDED Requirements

### Requirement: Canonical Skill Discovery Contract

The system SHALL discover runnable skills from canonical folder-based entries.

#### Scenario: Discovery for Composition and Routing

- GIVEN composition or orchestration needs to enumerate skills
- WHEN discovery runs
- THEN discovery SHALL use canonical skill folders with `SKILL.md` entry files
- AND discovery SHALL not require category-local `*.md` skill files.

### Requirement: Strict Cutover Without Legacy Support

The system SHALL enforce strict cutover to canonical skill identities for active composition and routing behavior.

#### Scenario: Legacy Reference Rejection

- GIVEN an active composition or routing input references a pre-flattened legacy skill path
- WHEN validation is applied
- THEN the reference SHALL be rejected as invalid for active behavior
- AND the run SHALL surface explicit validation errors.
