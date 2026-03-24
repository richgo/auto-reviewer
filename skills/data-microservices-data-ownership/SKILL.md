---
name: data microservices data ownership
description: >
  Data Ownership Violations. Use this skill whenever
  diffs may introduce data issues on microservices, especially in all. Actively look
  for: Multiple services writing to same table, unclear source of truth, sync conflicts.
  and report findings with medium severity expectations and actionable fixes.
---

# Data Ownership Violations
## Task Metadata
- Category: `data`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Multiple services writing to same table, unclear source of truth, sync conflicts.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Multiple services writing to same table, unclear source of truth, sync conflicts....

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
