---
name: data android content provider exposure
description: >
  Migrated review-task skill for ContentProvider Data Exposure. Use this skill whenever
  diffs may introduce data issues on mobile, especially in Kotlin, Java. Actively look
  for: Exported ContentProvider leaking app data, missing URI permission grants. and
  report findings with high severity expectations and actionable fixes.
---

# ContentProvider Data Exposure

## Source Lineage
- Original review task: `review-tasks/data/android/content-provider-exposure.md`
- Migrated skill artifact: `skills/review-task-data-android-content-provider-exposure/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Exported ContentProvider leaking app data, missing URI permission grants.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Exported ContentProvider leaking app data, missing URI permission grants....

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
