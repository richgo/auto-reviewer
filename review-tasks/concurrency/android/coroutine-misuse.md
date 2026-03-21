# Task: Android Coroutine Misuse

## Category
concurrency

## Severity
high

## Platforms
mobile

## Languages
Kotlin

## Description
Wrong dispatcher (Dispatchers.Main for I/O), leaked GlobalScope, missing structured concurrency.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases

### Case 1: Primary vulnerability
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Wrong dispatcher (Dispatchers.Main for I/O), leaked GlobalScope, missing structured concur...

### Case 2: Alternative pattern
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue via different approach.

## Counter-Examples

### Counter 1: Secure implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as high
- [ ] References relevant standards or guidelines
