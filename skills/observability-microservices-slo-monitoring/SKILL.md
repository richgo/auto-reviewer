---
name: observability microservices slo monitoring
description: >
  SLO Monitoring Missing. Use this skill whenever diffs
  may introduce observability issues on microservices, especially in all. Actively look
  for: No SLI/SLO definitions, missing error budget tracking, no alerting on latency
  percentiles. and report findings with medium severity expectations and actionable
  fixes.
---

# SLO Monitoring Missing
## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
No SLI/SLO definitions, missing error budget tracking, no alerting on latency percentiles.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No SLI/SLO definitions, missing error budget tracking, no alerting on latency percentiles....

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
