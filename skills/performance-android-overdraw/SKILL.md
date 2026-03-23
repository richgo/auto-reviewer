---
name: performance android overdraw
description: >
  Migrated review-task skill for Android Overdraw. Use this skill whenever diffs may
  introduce performance issues on mobile, especially in Kotlin, Java, XML. Actively look
  for: Nested backgrounds, redundant draw passes, missing clipRect optimization. and
  report findings with medium severity expectations and actionable fixes.
---

# Android Overdraw

## Source Lineage
- Original review task: `review-tasks/performance/android/overdraw.md`
- Migrated skill artifact: `skills/review-task-performance-android-overdraw/SKILL.md`

## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java, XML`

## Purpose
Nested backgrounds, redundant draw passes, missing clipRect optimization.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Nested backgrounds, redundant draw passes, missing clipRect optimization....

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
