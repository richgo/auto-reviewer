# composer-manifest Specification Delta

## ADDED Requirements

### Requirement: Repository-Aware Manifest Composition

The system SHALL generate a project-specific `apm.yml` by selecting auto-reviewer skill dependencies from detected repository signals.

#### Scenario: Generate Manifest for Detected Stack

- GIVEN a target repository with detectable language/platform/build/CI signals
- WHEN the composer runs in generate mode
- THEN it SHALL output an `apm.yml` containing auto-reviewer dependencies that match the detected stack profile
- AND it SHALL include required core dependencies regardless of detected stack

#### Scenario: Monorepo Union Selection

- GIVEN a monorepo containing multiple language or platform subprojects
- WHEN the composer scans the repository
- THEN it SHALL compose dependencies from the union of detected capabilities across subdirectories
- AND it SHALL avoid dropping dependencies needed by minority subprojects

### Requirement: Deterministic Dependency Ordering

The system SHALL produce deterministic dependency ordering for composer-managed entries.

#### Scenario: Stable Output Across Re-Runs

- GIVEN unchanged repository contents and unchanged composition inputs
- WHEN the composer is run multiple times
- THEN the generated composer-managed dependency list SHALL be identical across runs
- AND no semantically empty reordering diff SHALL be introduced

### Requirement: Version Pin Strategy

The system SHALL support explicit version reference strategies for generated auto-reviewer dependencies.

#### Scenario: Default Stable Pinning

- GIVEN no explicit reference override is provided
- WHEN the composer generates dependencies
- THEN each generated auto-reviewer dependency SHALL include a stable release ref
- AND the output SHALL be compatible with downstream lockfile resolution

#### Scenario: Explicit Ref Override

- GIVEN an explicit ref strategy or ref value is provided
- WHEN the composer generates dependencies
- THEN generated dependencies SHALL use that explicit strategy/value
- AND resulting refs SHALL remain syntactically valid for APM dependency notation

### Requirement: Update Mode with Scoped Merge

The system SHALL support update mode that refreshes composer-managed dependencies without overwriting unrelated manifest content.

#### Scenario: Preserve User-Managed Manifest Sections

- GIVEN an existing `apm.yml` containing user-managed configuration and non-auto-reviewer dependencies
- WHEN the composer runs in update mode
- THEN it SHALL update only composer-managed auto-reviewer dependency entries
- AND it SHALL preserve unrelated keys and non-managed dependency entries

### Requirement: Validation Before Persist

The system SHALL validate generated manifest content prior to writing.

#### Scenario: Reject Invalid Generated Dependency

- GIVEN generated output contains an invalid dependency path, invalid ref format, or invalid manifest shape
- WHEN validation runs
- THEN the composer SHALL fail the run with explicit errors
- AND it SHALL NOT write a partial or invalid `apm.yml`
