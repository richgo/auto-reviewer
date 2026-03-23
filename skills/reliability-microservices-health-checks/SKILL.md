---
name: reliability microservices health checks
description: >
  Migrated review-task skill for Health Check Misconfiguration. Use this skill whenever
  diffs may introduce reliability issues on microservices, especially in all. Actively
  look for: Liveness/readiness probes missing or wrong, health check not testing
  dependencies. and report findings with medium severity expectations and actionable
  fixes.
---

# Health Check Misconfiguration

## Source Lineage
- Original review task: `review-tasks/reliability/microservices/health-checks.md`
- Migrated skill artifact: `skills/review-task-reliability-microservices-health-checks/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Liveness/readiness probes missing or wrong, health check not testing dependencies.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Liveness/readiness probes missing or wrong, health check not testing dependencies....

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
