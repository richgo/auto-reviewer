---
name: concurrency android handler looper
description: >
  Migrated review-task skill for Android Handler/Looper Issues. Use this skill whenever
  diffs may introduce concurrency issues on mobile, especially in Kotlin, Java. Actively
  look for: Posting to dead Handler, missing Looper cleanup, leaked delayed messages.
  and report findings with medium severity expectations and actionable fixes.
---

# Android Handler/Looper Issues

## Source Lineage
- Original review task: `review-tasks/concurrency/android/handler-looper.md`
- Migrated skill artifact: `skills/review-task-concurrency-android-handler-looper/SKILL.md`

## Task Metadata
- Category: `concurrency`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Posting to dead Handler, missing Looper cleanup, leaked delayed messages.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases
### Case 1: Primary vulnerability
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Posting to dead Handler, missing Looper cleanup, leaked delayed messages....

### Case 2: Alternative pattern
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue via different approach.

## Counter-Examples
### Counter 1: Secure implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as medium
- [ ] References relevant standards or guidelines

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
