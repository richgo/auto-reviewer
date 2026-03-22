# review-tasks Specification Delta

## MODIFIED Requirements

### Requirement: Review Task Format

The system SHALL treat review-task artifacts as transitional migration inputs, not as active tuneable runtime units.

(Previously: The system defined review tasks as standalone markdown files with a structured template for ongoing use.)

#### Scenario: Transitional Task Usage

- GIVEN the flattened skill-first architecture is active
- WHEN review execution, tuning, or benchmarking runs
- THEN the system SHALL use skills as the active unit
- AND review-task artifacts SHALL not be required for runtime operation.

### Requirement: Taxonomy Structure

The system SHALL represent active review taxonomy through skills instead of a standalone review-task tree.

(Previously: The system organized review tasks by concern category with platform subfolders.)

#### Scenario: Taxonomy Resolution in Active Architecture

- GIVEN taxonomy coverage is audited
- WHEN concern and platform groupings are inspected
- THEN groupings SHALL be discoverable through skill organization and metadata
- AND taxonomy coverage SHALL not depend on a standalone review-task directory.

### Requirement: Eval Case Format

The system SHALL source executable eval behavior from skill-linked eval datasets.

(Previously: Each review task included testable eval cases and counter-examples in task files.)

#### Scenario: Eval Source of Truth

- GIVEN a capability is evaluated in benchmark or tuning workflows
- WHEN eval inputs are resolved
- THEN evals SHALL map to skills as the active source of truth
- AND task-local eval snippets SHALL not be required to execute evaluation workflows.

## REMOVED Requirements

### Requirement: Platform Coverage

(Reason: Platform-coverage obligations move from standalone review-task inventory counts to skill-level coverage guarantees in the flattened model.)

### Requirement: Severity Tagging

(Reason: Severity semantics remain required for review findings, but requirement ownership moves to active skill and output capabilities rather than task-level artifacts.)
