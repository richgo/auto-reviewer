---
name: correctness android lifecycle bugs
description: >
  Android Lifecycle Bugs. Use this skill whenever diffs
  may introduce correctness issues on mobile, especially in Kotlin, Java. Actively look
  for: Accessing views after onDestroyView, Fragment not attached, leaking Activity
  references. and report findings with high severity expectations and actionable fixes.
---

# Android Lifecycle Bugs
## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Accessing views after onDestroyView, Fragment not attached, leaking Activity references.

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
**Expected finding:** High — Accessing views after onDestroyView, Fragment not attached, leaking Activity ref...

### Case 2: Alternative manifestation
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

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
