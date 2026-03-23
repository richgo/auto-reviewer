# copilot-sdk-runtime-alignment Specification Delta

## ADDED Requirements

### Requirement: Copilot SDK-First Runtime Contract

The system SHALL define Copilot SDK as the default runtime transport for tuning and benchmark workflows in normative repository guidance.

#### Scenario: Normative Runtime Guidance

- GIVEN contributors read repository guidance for benchmark and tuning operations
- WHEN runtime/authentication defaults are specified
- THEN guidance SHALL describe Copilot SDK-oriented runtime expectations
- AND defaults SHALL NOT rely on unlabeled Claude CLI-only assumptions

### Requirement: Runtime Example Consistency

The system SHALL keep runtime examples and model identifiers consistent with the Copilot SDK-first contract.

#### Scenario: Example Command Review

- GIVEN repository examples for tuning and benchmark execution
- WHEN maintainers review model IDs and auth steps
- THEN examples SHALL use model identifiers and authentication flows compatible with Copilot SDK usage
- AND provider-specific examples SHALL be explicitly labeled when shown as alternatives

### Requirement: Historical Reference De-Emphasis

The system SHALL treat lingering Claude CLI references as non-normative historical context only.

#### Scenario: Mixed Historical Documentation

- GIVEN historical docs include Claude CLI references
- WHEN those docs coexist with active runtime guidance
- THEN active sections SHALL clearly prioritize Copilot SDK expectations
- AND historical Claude references SHALL be labeled as non-default context

