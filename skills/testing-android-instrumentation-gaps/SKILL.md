---
name: testing android instrumentation gaps
description: >
  Android Instrumentation Gaps. Use this skill whenever
  diffs may introduce testing issues on mobile, especially in Kotlin, Java. Actively
  look for: Database migrations untested, missing Robolectric for unit tests, no
  integration tests. and report findings with medium severity expectations and
  actionable fixes.
---

# Android Instrumentation Gaps
## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Database migrations untested, missing Robolectric for unit tests, no integration tests.

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
**Expected finding:** Medium — Database migrations untested, missing Robolectric for unit tests, no integration...

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
