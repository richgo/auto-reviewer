---
name: data serialization mismatch
description: >
  Serialization Mismatch. Use this skill whenever diffs
  may introduce data issues on all, especially in all. Actively look for: Type changes
  breaking serialization, missing schema evolution, backwards incompatible formats. and
  report findings with medium severity expectations and actionable fixes.
---

# Serialization Mismatch
## Task Metadata
- Category: `data`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Type changes breaking serialization, missing schema evolution, backwards incompatible formats.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Type changes breaking serialization, missing schema evolution, backwards incompatible form...

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
