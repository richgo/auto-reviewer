---
name: review-task-observability-android-anr-detection
description: >
  Migrated review-task skill for ANR Detection Missing. Use this skill whenever diffs
  may introduce observability issues on mobile, especially in Kotlin, Java. Actively
  look for: No ANR monitoring, missing StrictMode in debug, no main thread watchdog. and
  report findings with medium severity expectations and actionable fixes.
---

# ANR Detection Missing

## Source Lineage
- Original review task: `review-tasks/observability/android/anr-detection.md`
- Migrated skill artifact: `skills/review-task-observability-android-anr-detection/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
No ANR monitoring, missing StrictMode in debug, no main thread watchdog.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No ANR monitoring, missing StrictMode in debug, no main thread watchdog....

### Case 2: Alternative scenario
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

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
