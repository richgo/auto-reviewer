# agent-composition Specification Delta

## ADDED Requirements

### Requirement: Agent-as-Skill-Group Contract

The system SHALL define agents as compositional wrappers that group and execute skills.

#### Scenario: Agent Composition Declaration

- GIVEN an agent capability is defined
- WHEN its contract is declared
- THEN the agent SHALL identify or select a set of skills to run
- AND the agent contract SHALL not introduce a separate tuneable primitive below skills.

### Requirement: Subagent Compatibility at Skill Layer

The system SHALL support subagent execution while preserving skill-level atomicity.

#### Scenario: Subagent Delegation

- GIVEN an agent delegates work to a subagent
- WHEN the delegated work is resolved
- THEN the delegated scope SHALL resolve to skill execution responsibilities
- AND reporting from delegation SHALL remain attributable to skill-level outputs.

### Requirement: Composition Policy Uses Skill Dependencies

The system SHALL express composition policy in terms of skill dependencies.

#### Scenario: Signal-Driven Composition

- GIVEN repository signals are detected for composition
- WHEN dependencies are selected
- THEN selected dependencies SHALL refer to skill paths
- AND policy evaluation SHALL not require standalone review-task dependencies.

### Requirement: Agent Output Traceability to Skills

The system SHALL enable traceability from agent outputs to the skills that produced them.

#### Scenario: Review Output Attribution

- GIVEN a review output produced by an agent flow
- WHEN output metadata or routing context is inspected
- THEN the output SHALL be attributable to participating skills
- AND attribution SHALL not require standalone review-task lineage.
