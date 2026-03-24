---
name: reliability android crash handling
description: >
  Android Crash Handling. Use this skill whenever diffs
  may introduce reliability issues on mobile, especially in Kotlin, Java. Actively look
  for: Uncaught exception handler not set, no graceful crash recovery, missing
  breadcrumbs. and report findings with medium severity expectations and actionable
  fixes.
---

# Android Crash Handling
## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Uncaught exception handler not set, no graceful crash recovery, missing breadcrumbs.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Uncaught exception handler not set, no graceful crash recovery, missing breadcrumbs....

### Case 2: Alternative pattern
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Issue manifests differently but same root cause.

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
