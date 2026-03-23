# review-tasks Specification Delta

## MODIFIED Requirements

### Requirement: Transitional Migration Inputs Only

The system SHALL treat review-task artifacts as historical migration inputs, while active skill identity is governed exclusively by canonical skill folders.

(Previously: review-task artifacts were historical migration inputs; this change clarifies that canonical foldered skills are the exclusive active identity contract.)

#### Scenario: Runtime Independence from Review-Task Trees

- GIVEN benchmark, tuning, composition, or orchestration workflows execute
- WHEN runtime inputs are resolved
- THEN active skill identity SHALL be resolved through canonical skill folders
- AND standalone review-task trees SHALL not be required for active runtime behavior.

### Requirement: Historical Taxonomy Context

The system SHALL retain review-task taxonomies only as historical, non-normative context and SHALL not use nested review-task folders to define active skill identity.

(Previously: historical labeling was required, but this change explicitly prohibits nested review-task trees from defining active identity.)

#### Scenario: Historical Inspection Boundaries

- GIVEN users inspect retained review-task taxonomy artifacts
- WHEN they compare those artifacts with active capabilities
- THEN taxonomy artifacts SHALL be interpretable as historical lineage only
- AND active skill identity SHALL be determined by canonical flattened skill folders.

## ADDED Requirements

### Requirement: Flattened Lineage Interpretability

The system SHALL preserve interpretability of historical nested lineage within canonical flattened skill identifiers.

#### Scenario: Nested-to-Flat Lineage Clarity

- GIVEN a historical nested lineage (for example `api-design/mobile`)
- WHEN active skill identity is inspected
- THEN the corresponding canonical identifier SHALL preserve lineage meaning (for example `api-design-mobile`)
- AND active lineage interpretation SHALL not require nested runtime folders.
