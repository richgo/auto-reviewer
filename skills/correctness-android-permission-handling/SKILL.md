---
name: correctness android permission handling
description: >
  Android Permission Handling. Use this skill whenever
  diffs may introduce correctness issues on mobile, especially in Kotlin, Java. Actively
  look for: Missing runtime permission checks (M+), assuming permissions granted, not
  handling denial. and report findings with medium severity expectations and actionable
  fixes.
---

# Android Permission Handling
## Task Metadata
- Category: `correctness`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Missing runtime permission checks (M+), assuming permissions granted, not handling denial.

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
**Expected finding:** Medium — Missing runtime permission checks (M+), assuming permissions granted, not handli...

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
