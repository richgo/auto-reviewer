---
name: review-task-api-design-breaking-api-change
description: >
  Migrated review-task skill for Breaking API Change. Use this skill whenever diffs may
  introduce api-design issues on all, especially in all. Actively look for: Removing
  fields, changing types, or renaming without versioning or deprecation period. and
  report findings with high severity expectations and actionable fixes.
---

# Breaking API Change

## Source Lineage
- Original review task: `review-tasks/api-design/breaking-api-change.md`
- Migrated skill artifact: `skills/review-task-api-design-breaking-api-change/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Removing fields, changing types, or renaming without versioning or deprecation period.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Removing fields, changing types, or renaming without versioning or deprecation period....

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

## Counter-Examples
### Counter 1: Proper implementation
```java
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
