# Task: Android Process Death

## Category
reliability

## Severity
high

## Platforms
mobile

## Languages
Kotlin, Java

## Description
State lost when OS kills process, missing SavedStateHandle, non-restorable navigation.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases

### Case 1: Problem demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — State lost when OS kills process, missing SavedStateHandle, non-restorable navigation...

### Case 2: Alternative pattern
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Issue manifests differently but same root cause.

## Counter-Examples

### Counter 1: Optimized implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Uses efficient algorithms and proper resource management.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific improvements
