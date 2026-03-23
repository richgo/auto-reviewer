---
name: correctness android config change crash
description: >
  Migrated review-task skill for Android Configuration Change Crashes. Use this skill
  whenever diffs may introduce correctness issues on mobile, especially in Kotlin, Java.
  Actively look for: State lost on rotation, ViewModel not used, non-parcelable data in
  Bundle. and report findings with high severity expectations and actionable fixes.
---

# Android Configuration Change Crashes

## Source Lineage
- Original review task: `review-tasks/correctness/android/config-change-crash.md`
- Migrated skill artifact: `skills/review-task-correctness-android-config-change-crash/SKILL.md`

## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
State lost on rotation, ViewModel not used, non-parcelable data in Bundle.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — State lost on rotation, ViewModel not used, non-parcelable data in Bundle....

### Case 2: Alternative manifestation
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
