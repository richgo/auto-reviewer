---
name: testing android ui test gaps
description: >
  Migrated review-task skill for Android UI Test Coverage Gaps. Use this skill whenever
  diffs may introduce testing issues on mobile, especially in Kotlin, Java. Actively
  look for: Critical UI flows untested, missing Espresso/Compose tests, no screenshot
  regression tests. and report findings with medium severity expectations and actionable
  fixes.
---

# Android UI Test Coverage Gaps

## Source Lineage
- Original review task: `review-tasks/testing/android/ui-test-gaps.md`
- Migrated skill artifact: `skills/review-task-testing-android-ui-test-gaps/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Critical UI flows untested, missing Espresso/Compose tests, no screenshot regression tests.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Critical UI flows untested, missing Espresso/Compose tests, no screenshot regres...

### Case 2: Alternative manifestation
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```kotlin
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
