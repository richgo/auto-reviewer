---
name: review-task-api-design-microservices-coupling
description: >
  Migrated review-task skill for Tight Coupling. Use this skill whenever diffs may
  introduce api-design issues on microservices, especially in all. Actively look for:
  Shared database between services, point-to-point REST instead of events, temporal
  coupling. and report findings with medium severity expectations and actionable fixes.
---

# Tight Coupling

## Source Lineage
- Original review task: `review-tasks/api-design/microservices/coupling.md`
- Migrated skill artifact: `skills/review-task-api-design-microservices-coupling/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Shared database between services, point-to-point REST instead of events, temporal coupling.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Shared database between services, point-to-point REST instead of events, temporal coupling...

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
