# Tuning Specification Delta

## ADDED Requirements

### Requirement: Autoresearch Tuning Approach

The system SHALL enable continuous skill improvement via autoresearch loops.

#### Scenario: Tuning Loop Architecture

- GIVEN skills need optimization over time
- WHEN running the tuning loop
- THEN it SHALL: run benchmark-runner to identify failing eval cases, analyze failure modes, mutate skill prompts/detection logic, re-run benchmarks, commit improved skills if metrics improve
- AND the loop SHALL be idempotent and safe (no destructive changes without validation)

### Requirement: Skill Optimizer

The system SHALL implement a skill-optimizer skill for automated prompt refinement.

#### Scenario: Optimizer Workflow

- GIVEN a skill has suboptimal precision or recall
- WHEN running the skill-optimizer
- THEN it SHALL: read eval failure logs, identify patterns (e.g., "always misses X pattern", "false positives on Y"), generate candidate mutations (add/remove heuristics, adjust severity, refine examples), test each mutation against evals, select the best-performing variant
- AND mutations SHALL be git-committed with clear messages describing the improvement

### Requirement: Benchmark Runner

The system SHALL implement a benchmark-runner skill for automated skill testing.

#### Scenario: Benchmark Execution

- GIVEN skills need performance measurement
- WHEN running the benchmark-runner
- THEN it SHALL: load all eval JSON files, execute each skill against corresponding test cases, compare actual findings to expected_findings, calculate precision/recall/F1/false positive rate per skill, generate a performance report
- AND the runner SHALL support filtering by skill, language, severity, or platform

#### Scenario: Assertion Checking

- GIVEN eval cases have assertions
- WHEN checking results
- THEN the benchmark-runner SHALL: verify must_detect: true cases are flagged, verify must_not_detect: true cases are NOT flagged, check severity matches expected severity, validate additional assertions (e.g., suggest_parameterized_query)
- AND assertion failures SHALL be logged with details (skill, test case id, expected vs actual)

### Requirement: Local Calibration

The system SHALL implement a local-calibration skill for repo-specific tuning.

#### Scenario: Repo Adaptation

- GIVEN each repository has unique conventions (naming, architecture, patterns)
- WHEN running local-calibration
- THEN it SHALL: analyze historical PR review comments, extract repo-specific rules (e.g., "always use logger.info, never print()"), identify commonly flagged false positives, generate calibration config, apply config to skill execution
- AND calibration SHALL be stored per-repo and versioned

### Requirement: Performance Reporting

The system SHALL generate detailed reports from tuning runs.

#### Scenario: Report Contents

- GIVEN a tuning run completes
- WHEN generating the report
- THEN it SHALL include: overall precision/recall/F1 per skill, breakdown by language/platform/severity, top false positives and false negatives, recommended skill improvements, historical trend (if available)
- AND reports SHALL be markdown files suitable for PR comments or documentation

### Requirement: Tuning Safety

The system SHALL prevent destructive changes during tuning.

#### Scenario: Safe Mutations

- GIVEN skill optimizer mutates prompts
- WHEN applying mutations
- THEN it SHALL: create a new branch for testing, run full benchmark suite on mutated skills, require metric improvement (precision +X%, recall +Y%) before merging, revert automatically if metrics degrade
- AND manual review SHALL be required for major changes (>10 line diff in skill)
