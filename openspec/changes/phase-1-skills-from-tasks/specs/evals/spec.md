# Evals Specification Delta

## ADDED Requirements

### Requirement: Eval Infrastructure Format

The system SHALL define eval test cases in structured JSON files for automated validation.

#### Scenario: Eval File Structure

- GIVEN skills need automated testing
- WHEN creating eval files
- THEN they SHALL be JSON files under evals/ directory organized by concern (e.g., evals/security-injection.json, evals/concurrency.json)
- AND each file SHALL contain an array of eval cases with required fields: id, skill, language, severity, code snippet, expected findings, assertions

### Requirement: Eval Case Structure

The system SHALL include eval cases with buggy code and expected findings.

#### Scenario: Eval Case Fields

- GIVEN an eval case is created
- WHEN defining the test case
- THEN it SHALL include: unique id (concern-category-NNN), skill reference, language, severity, code snippet (buggy code), expected_findings (array of findings with type and optional line number)
- AND it SHALL include assertions: must_detect (boolean), severity (expected severity level), additional checks (e.g., suggest_parameterized_query for SQL injection)

#### Example:
```json
{
  "id": "sql-injection-001",
  "skill": "security-injection",
  "language": "python",
  "severity": "critical",
  "code": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
  "expected_findings": [{"type": "sql-injection", "line": 1}],
  "assertions": {
    "must_detect": true,
    "severity": "critical",
    "suggest_parameterized_query": true
  }
}
```

### Requirement: Counter-Example Structure

The system SHALL include counter-examples showing correct code that should NOT be flagged.

#### Scenario: Counter-Example Fields

- GIVEN false positives need to be prevented
- WHEN creating counter-examples
- THEN they SHALL include: unique id, skill reference, language, code snippet (correct code), expected_findings (empty array or null), assertions.must_not_detect: true
- AND counter-examples SHALL test similar but safe patterns to eval cases

#### Example:
```json
{
  "id": "sql-injection-counter-001",
  "skill": "security-injection",
  "language": "python",
  "code": "query = \"SELECT * FROM users WHERE id = ?\"\nparams = (user_id,)",
  "expected_findings": [],
  "assertions": {
    "must_not_detect": true
  }
}
```

### Requirement: Eval Coverage

The system SHALL provide eval cases for all concern skills.

#### Scenario: Concern Skill Coverage

- GIVEN 19 concern skills exist
- WHEN creating eval files
- THEN each concern skill SHALL have a corresponding evals/{skill}.json file
- AND each file SHALL include at least 2-3 eval cases
- AND each file SHALL include at least 1-2 counter-examples

### Requirement: Scoring Rubric

The system SHALL define scoring metrics for skill performance.

#### Scenario: Metrics Definition

- GIVEN skill performance needs measurement
- WHEN evaluating skills against test cases
- THEN the benchmark-runner SHALL calculate: precision (true positives / (true positives + false positives)), recall (true positives / (true positives + false negatives)), F1 score (harmonic mean of precision and recall), false positive rate
- AND skills SHALL meet minimum thresholds: precision >90%, recall >80%

### Requirement: Eval Extraction from Review Tasks

The system SHALL extract eval cases from Phase 0 review task files.

#### Scenario: Automated Extraction

- GIVEN review tasks contain inline eval cases
- WHEN building eval JSON files
- THEN eval cases SHALL be extracted programmatically from review task markdown files
- AND extraction SHALL preserve: code snippets, expected findings, counter-examples
- AND eval id SHALL map to the source review task
