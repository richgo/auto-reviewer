---
name: review-task-reliability-android-offline-resilience
description: >
  Migrated review-task skill for Android Offline Resilience. Use this skill whenever
  diffs may introduce reliability issues on mobile, especially in Kotlin, Java. Actively
  look for: No offline queue, crashes on network unavailable, missing
  ConnectivityManager checks. and report findings with medium severity expectations and
  actionable fixes.
---

# Android Offline Resilience

## Source Lineage
- Original review task: `review-tasks/reliability/android/offline-resilience.md`
- Migrated skill artifact: `skills/review-task-reliability-android-offline-resilience/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
No offline queue, crashes on network unavailable, missing ConnectivityManager checks.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No offline queue, crashes on network unavailable, missing ConnectivityManager checks....

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
