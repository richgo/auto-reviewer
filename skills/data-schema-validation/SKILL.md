---
name: review-task-data-schema-validation
description: >
  Migrated review-task skill for Schema Validation Missing. Use this skill whenever
  diffs may introduce data issues on web, api, microservices, especially in all.
  Actively look for: No JSON schema validation on API inputs, accepting malformed data.
  and report findings with medium severity expectations and actionable fixes.
---

# Schema Validation Missing

## Source Lineage
- Original review task: `review-tasks/data/schema-validation.md`
- Migrated skill artifact: `skills/review-task-data-schema-validation/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `medium`
- Platforms: `web, api, microservices`
- Languages: `all`

## Purpose
No JSON schema validation on API inputs, accepting malformed data.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No JSON schema validation on API inputs, accepting malformed data....

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

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
