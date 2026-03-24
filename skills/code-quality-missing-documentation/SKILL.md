---
name: code quality missing documentation
description: >
  Missing Documentation. Use this skill whenever diffs
  may introduce code-quality issues on all, especially in all. Actively look for: Public
  APIs without docstrings, complex logic without comments, missing README. and report
  findings with low severity expectations and actionable fixes.
---

# Missing Documentation
## Task Metadata
- Category: `code-quality`
- Severity: `low`
- Platforms: `all`
- Languages: `all`

## Purpose
Public APIs without docstrings, complex logic without comments, missing README.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Public APIs without docstrings, complex logic without comments, missing README....

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Similar issue in different context.

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
