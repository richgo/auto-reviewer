---
name: observability android crash reporting
description: >
  Migrated review-task skill for Android Crash Reporting Gaps. Use this skill whenever
  diffs may introduce observability issues on mobile, especially in Kotlin, Java.
  Actively look for: Missing Crashlytics/Sentry, no breadcrumbs, obfuscated stacktraces
  without ProGuard mapping. and report findings with medium severity expectations and
  actionable fixes.
---

# Android Crash Reporting Gaps

## Source Lineage
- Original review task: `review-tasks/observability/android/crash-reporting.md`
- Migrated skill artifact: `skills/review-task-observability-android-crash-reporting/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Missing Crashlytics/Sentry, no breadcrumbs, obfuscated stacktraces without ProGuard mapping.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing Crashlytics/Sentry, no breadcrumbs, obfuscated stacktraces without ProGuard mappin...

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
