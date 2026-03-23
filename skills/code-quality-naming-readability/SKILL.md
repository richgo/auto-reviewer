---
name: code quality naming readability
description: >
  Migrated review-task skill for Naming and Readability. Use this skill whenever diffs
  may introduce code-quality issues on all, especially in all. Actively look for:
  Unclear variable names, single-letter vars outside loops, misleading function names.
  and report findings with low severity expectations and actionable fixes.
---

# Naming and Readability

## Source Lineage
- Original review task: `review-tasks/code-quality/naming-readability.md`
- Migrated skill artifact: `skills/review-task-code-quality-naming-readability/SKILL.md`

## Task Metadata
- Category: `code-quality`
- Severity: `low`
- Platforms: `all`
- Languages: `all`

## Purpose
Unclear variable names, single-letter vars outside loops, misleading function names.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Unclear variable names, single-letter vars outside loops, misleading function names....

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Similar issue in different context.

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
