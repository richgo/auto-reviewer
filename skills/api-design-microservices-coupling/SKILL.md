---
name: api design microservices coupling
description: >
  Tight Coupling. Use this skill whenever diffs may
  introduce api-design issues on microservices, especially in all. Actively look for:
  Shared database between services, point-to-point REST instead of events, temporal
  coupling. and report findings with medium severity expectations and actionable fixes.
---

# Tight Coupling
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
