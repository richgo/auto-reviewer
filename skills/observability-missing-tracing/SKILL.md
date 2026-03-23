---
name: review-task-observability-missing-tracing
description: >
  Migrated review-task skill for Missing Distributed Tracing. Use this skill whenever
  diffs may introduce observability issues on microservices, especially in all. Actively
  look for: No trace propagation across services, missing correlation IDs, can't debug
  cross-service issues. and report findings with medium severity expectations and
  actionable fixes.
---

# Missing Distributed Tracing

## Source Lineage
- Original review task: `review-tasks/observability/missing-tracing.md`
- Migrated skill artifact: `skills/review-task-observability-missing-tracing/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
No trace propagation across services, missing correlation IDs, can't debug cross-service issues.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No trace propagation across services, missing correlation IDs, can't debug cross-service i...

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
