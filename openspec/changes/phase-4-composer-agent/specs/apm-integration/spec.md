# apm-integration Specification Delta

## ADDED Requirements

### Requirement: Install and Compile Readiness

The system SHALL generate manifests that are directly usable by APM install/compile flows.

#### Scenario: Ready for Install After Compose

- GIVEN compose successfully generated or updated `apm.yml`
- WHEN a user runs `apm install`
- THEN the dependency list SHALL be parseable by APM
- AND lockfile resolution SHALL proceed without requiring manual manifest fixes

#### Scenario: Runtime Compilation Compatibility

- GIVEN a composed manifest for a repository with one or more detected runtimes
- WHEN a user runs `apm compile`
- THEN APM compilation SHALL receive dependency and compilation settings compatible with the detected runtime profile
- AND generated agent instruction artifacts SHALL correspond to selected dependencies

### Requirement: Multi-Runtime Compilation Defaults

The system SHALL support multi-runtime repositories through compilation defaults in composed manifests.

#### Scenario: Multi-Runtime Repository

- GIVEN a repository with signals for multiple supported agent runtimes
- WHEN composition generates the manifest
- THEN compilation-related manifest fields SHALL be set to support multi-runtime output
- AND the defaults SHALL not block single-runtime repositories from compiling

### Requirement: Ref and Lockfile Compatibility

The system SHALL ensure generated dependency refs remain compatible with lockfile semantics.

#### Scenario: Locked Resolution with Pinned Refs

- GIVEN generated dependencies include explicit refs
- WHEN `apm install` resolves and writes lock data
- THEN lock entries SHALL correspond to generated dependencies and refs
- AND repeated install with unchanged manifest SHALL preserve dependency intent
