---
name: testing test isolation
description: >
  Migrated review-task skill for Test Isolation Failures. Use this skill whenever diffs
  may introduce testing issues on all, especially in all. Actively look for: Tests
  sharing mutable state, order-dependent tests, missing cleanup between tests. and
  report findings with medium severity expectations and actionable fixes.
---

# Test Isolation Failures

## Source Lineage
- Original review task: `review-tasks/testing/test-isolation.md`
- Migrated skill artifact: `skills/review-task-testing-test-isolation/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Tests sharing mutable state, order-dependent tests, missing cleanup between tests.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Tests sharing mutable state, order-dependent tests, missing cleanup between test...

### Case 2: Alternative manifestation
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
