---
name: reliability android crash handling
description: >
  Migrated review-task skill for Android Crash Handling. Use this skill whenever diffs
  may introduce reliability issues on mobile, especially in Kotlin, Java. Actively look
  for: Uncaught exception handler not set, no graceful crash recovery, missing
  breadcrumbs. and report findings with medium severity expectations and actionable
  fixes.
---

# Android Crash Handling

## Source Lineage
- Original review task: `review-tasks/reliability/android/crash-handling.md`
- Migrated skill artifact: `skills/review-task-reliability-android-crash-handling/SKILL.md`

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
