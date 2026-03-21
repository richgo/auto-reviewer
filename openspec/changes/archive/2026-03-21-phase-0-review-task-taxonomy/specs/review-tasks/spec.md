# Review Tasks Specification Delta

## ADDED Requirements

### Requirement: Review Task Format

The system SHALL define review tasks as standalone markdown files with a structured template.

#### Scenario: Task File Structure

- GIVEN a code review concern needs to be detected
- WHEN creating a review task file
- THEN it SHALL include: name, severity, description, detection heuristics, OWASP mapping (where applicable), eval cases (buggy code + expected finding), counter-examples (correct code that should not be flagged), fix guidance, and applicable platforms/languages
- AND the file SHALL be under 500 lines with references/ subdirectory for additional detail

### Requirement: Taxonomy Structure

The system SHALL organize review tasks by concern category with platform subfolders.

#### Scenario: Platform Subfolder Convention

- GIVEN a review task is platform-specific
- WHEN organizing the task file
- THEN it SHALL be placed under the category folder in a platform subdirectory (android/, ios/, web/, microservices/)
- AND tasks at the category root level SHALL be truly universal (applicable across all platforms)
- AND this convention SHALL apply consistently across all 10 concern categories

#### Scenario: Concern Categories

- GIVEN the comprehensive taxonomy of code review concerns
- WHEN organizing review tasks
- THEN they SHALL be grouped into: Security, Concurrency, Correctness, Testing, Performance, Reliability, API Design, Data, Observability, Code Quality
- AND Security SHALL be further subdivided into: Injection, Auth & Session, Data Protection, Network & Transport, Cookie & Client-Side, API & GraphQL, AI & LLM, Supply Chain, DoS, Infrastructure, Android, iOS, Mobile Shared, Web-Specific, Logging & Errors, Microservices

### Requirement: OWASP Mapping

The system SHALL map every security task to relevant OWASP CheatSheetSeries documents.

#### Scenario: OWASP Tag Format

- GIVEN a security-related review task
- WHEN creating the task file
- THEN it SHALL include `[OWASP: CheatSheetName, AnotherCheatSheet]` tags referencing the relevant OWASP cheat sheets
- AND mobile security tasks SHALL additionally reference MASVS control groups where applicable

### Requirement: Eval Case Format

The system SHALL include testable eval cases and counter-examples in each review task.

#### Scenario: Eval Case Structure

- GIVEN a review task needs to be independently testable
- WHEN defining eval cases
- THEN each task SHALL include 2-3 eval cases with buggy code snippets and expected findings
- AND each task SHALL include 1-2 counter-examples showing similar but correct code that should NOT be flagged
- AND eval cases SHALL be extractable for automated testing

### Requirement: Platform Coverage

The system SHALL provide comprehensive coverage across mobile, web, and distributed system platforms.

#### Scenario: Platform-Specific Tasks

- GIVEN the taxonomy covers multiple platforms
- WHEN reviewing the task inventory
- THEN it SHALL include: 28 Android-specific tasks, 28 iOS-specific tasks, 35+ web-specific tasks, 32 microservices-specific tasks, 8 mobile-shared tasks
- AND 58 general tasks SHALL apply across all platforms
- AND total coverage SHALL include 197 tasks

### Requirement: Severity Tagging

The system SHALL classify each review task by severity.

#### Scenario: Severity Levels

- GIVEN a review task is created
- WHEN assigning severity
- THEN it SHALL use one of: critical, high, medium, low
- AND severity SHALL guide prioritization in review reports
