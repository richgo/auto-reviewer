---
name: reliability android process death
description: >
  Android Process Death. Use this skill whenever diffs
  may introduce reliability issues on mobile, especially in Kotlin, Java. Actively look
  for: State lost when OS kills process, missing SavedStateHandle, non-restorable
  navigation. and report findings with high severity expectations and actionable fixes.
---

# Android Process Death
## Task Metadata
- Category: `reliability`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
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
