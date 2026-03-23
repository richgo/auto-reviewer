---
name: api design mobile excessive data fetch
description: >
  Migrated review-task skill for Excessive Data Fetch. Use this skill whenever diffs may
  introduce api-design issues on mobile, especially in Swift, Kotlin. Actively look for:
  Downloading full payloads on cellular, missing pagination/field selection for mobile.
  and report findings with medium severity expectations and actionable fixes.
---

# Excessive Data Fetch

## Source Lineage
- Original review task: `review-tasks/api-design/mobile/excessive-data-fetch.md`
- Migrated skill artifact: `skills/review-task-api-design-mobile-excessive-data-fetch/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Kotlin`

## Purpose
Downloading full payloads on cellular, missing pagination/field selection for mobile.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Downloading full payloads on cellular, missing pagination/field selection for mobile....

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
