---
name: code quality microservices api documentation
description: >
  API Documentation Missing. Use this skill whenever
  diffs may introduce code-quality issues on microservices, especially in all. Actively
  look for: No OpenAPI spec, missing endpoint documentation, undocumented error codes.
  and report findings with medium severity expectations and actionable fixes.
---

# API Documentation Missing
## Task Metadata
- Category: `code-quality`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
No OpenAPI spec, missing endpoint documentation, undocumented error codes.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No OpenAPI spec, missing endpoint documentation, undocumented error codes....

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
