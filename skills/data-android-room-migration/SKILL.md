---
name: review-task-data-android-room-migration
description: >
  Migrated review-task skill for Android Room Migration Issues. Use this skill whenever
  diffs may introduce data issues on mobile, especially in Kotlin, Java. Actively look
  for: Destructive Room migration, missing Migration objects, schema hash mismatch
  crashes. and report findings with high severity expectations and actionable fixes.
---

# Android Room Migration Issues

## Source Lineage
- Original review task: `review-tasks/data/android/room-migration.md`
- Migrated skill artifact: `skills/review-task-data-android-room-migration/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Destructive Room migration, missing Migration objects, schema hash mismatch crashes.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Destructive Room migration, missing Migration objects, schema hash mismatch crashes....

### Case 2: Alternative scenario
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

## Counter-Examples
### Counter 1: Proper implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Provides actionable recommendation

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
