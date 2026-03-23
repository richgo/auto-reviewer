---
name: review-task-observability-missing-metrics
description: >
  Migrated review-task skill for Missing Metrics. Use this skill whenever diffs may
  introduce observability issues on web, api, microservices, especially in all. Actively
  look for: No instrumentation for SLIs (latency, error rate, throughput), missing
  business metrics. and report findings with medium severity expectations and actionable
  fixes.
---

# Missing Metrics

## Source Lineage
- Original review task: `review-tasks/observability/missing-metrics.md`
- Migrated skill artifact: `skills/review-task-observability-missing-metrics/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `web, api, microservices`
- Languages: `all`

## Purpose
No instrumentation for SLIs (latency, error rate, throughput), missing business metrics.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No instrumentation for SLIs (latency, error rate, throughput), missing business metrics....

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
