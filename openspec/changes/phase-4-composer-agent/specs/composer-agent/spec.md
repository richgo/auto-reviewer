# composer-agent Specification Delta

## ADDED Requirements

### Requirement: Agent-Driven Compose Entry

The system SHALL provide an agent-driven entrypoint that can generate `apm.yml` from repository context.

#### Scenario: Compose via Agent Instruction

- GIVEN an environment that supports the project agent instruction format
- WHEN a user invokes the compose command through the composer agent
- THEN the agent SHALL produce a candidate `apm.yml` for the target repository
- AND the candidate SHALL conform to the composer-managed manifest contract

### Requirement: Policy-Constrained Agent Output

The system SHALL constrain agent-generated selections to an approved mapping policy.

#### Scenario: Agent Output Outside Policy

- GIVEN the agent proposes dependencies not allowed by composition policy
- WHEN policy validation is applied
- THEN non-compliant dependencies SHALL be rejected
- AND the compose run SHALL surface policy errors rather than silently accepting out-of-policy output

### Requirement: Safety Fallback for Weak Detection

The system SHALL produce a safe baseline when repository detection signals are sparse or ambiguous.

#### Scenario: Minimal Signal Repository

- GIVEN a repository with insufficient stack detection signals
- WHEN composition runs
- THEN the output SHALL include a minimal core baseline dependency set
- AND the result SHALL indicate limited detection confidence

### Requirement: Compositional Re-run Workflow

The system SHALL support re-running composition after repository changes.

#### Scenario: Recompose After Stack Change

- GIVEN a repository has added new stack/platform signals since the last compose run
- WHEN compose is re-run in update mode
- THEN the manifest SHALL include newly required dependencies for the added capabilities
- AND previously still-relevant dependencies SHALL be retained
