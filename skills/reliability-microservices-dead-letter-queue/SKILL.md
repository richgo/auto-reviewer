---
name: review-task-reliability-microservices-dead-letter-queue
description: >
  Migrated review-task skill for Dead Letter Queue Missing. Use this skill whenever
  diffs may introduce reliability issues on microservices, especially in all. Actively
  look for: Failed messages silently dropped, no DLQ monitoring, poison pill handling
  missing. and report findings with medium severity expectations and actionable fixes.
---

# Dead Letter Queue Missing

## Source Lineage
- Original review task: `review-tasks/reliability/microservices/dead-letter-queue.md`
- Migrated skill artifact: `skills/review-task-reliability-microservices-dead-letter-queue/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Failed messages silently dropped, no DLQ monitoring, poison pill handling missing.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Failed messages silently dropped, no DLQ monitoring, poison pill handling missing....

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Issue manifests differently but same root cause.

## Counter-Examples
### Counter 1: Optimized implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Uses efficient algorithms and proper resource management.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific improvements

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
