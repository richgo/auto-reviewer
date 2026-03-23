---
name: performance microservices latency chain
description: >
  Migrated review-task skill for Latency Chain. Use this skill whenever diffs may
  introduce performance issues on microservices, especially in all. Actively look for:
  Sequential synchronous calls across services (waterfall), missing parallelization. and
  report findings with high severity expectations and actionable fixes.
---

# Latency Chain

## Source Lineage
- Original review task: `review-tasks/performance/microservices/latency-chain.md`
- Migrated skill artifact: `skills/review-task-performance-microservices-latency-chain/SKILL.md`

## Task Metadata
- Category: `performance`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Sequential synchronous calls across services (waterfall), missing parallelization.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Sequential synchronous calls across services (waterfall), missing parallelization....

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Issue manifests differently but same root cause.

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
