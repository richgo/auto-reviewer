---
name: review-task-reliability-graceful-degradation
description: >
  Migrated review-task skill for Graceful Degradation Missing. Use this skill whenever
  diffs may introduce reliability issues on web, microservices, especially in all.
  Actively look for: Hard failures instead of fallbacks, no feature flags for
  degradation. and report findings with medium severity expectations and actionable
  fixes.
---

# Graceful Degradation Missing

## Source Lineage
- Original review task: `review-tasks/reliability/graceful-degradation.md`
- Migrated skill artifact: `skills/review-task-reliability-graceful-degradation/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `web, microservices`
- Languages: `all`

## Purpose
Hard failures instead of fallbacks, no feature flags for degradation.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Hard failures instead of fallbacks, no feature flags for degradation....

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
