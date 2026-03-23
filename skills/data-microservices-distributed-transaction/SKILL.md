---
name: review-task-data-microservices-distributed-transaction
description: >
  Migrated review-task skill for Distributed Transaction Issues. Use this skill whenever
  diffs may introduce data issues on microservices, especially in all. Actively look
  for: 2PC across services (fragile), missing saga pattern, no compensation on failure.
  and report findings with high severity expectations and actionable fixes.
---

# Distributed Transaction Issues

## Source Lineage
- Original review task: `review-tasks/data/microservices/distributed-transaction.md`
- Migrated skill artifact: `skills/review-task-data-microservices-distributed-transaction/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
2PC across services (fragile), missing saga pattern, no compensation on failure.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — 2PC across services (fragile), missing saga pattern, no compensation on failure....

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
