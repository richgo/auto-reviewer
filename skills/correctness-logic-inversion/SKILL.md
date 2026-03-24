---
name: correctness logic inversion
description: >
  Logic Inversion. Use this skill whenever diffs may
  introduce correctness issues on all, especially in all. Actively look for: Boolean
  logic errors, negation mistakes, De Morgan's law violations. and report findings with
  medium severity expectations and actionable fixes.
---

# Logic Inversion
## Task Metadata
- Category: `correctness`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Boolean logic errors, negation mistakes, De Morgan's law violations.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Boolean logic errors, negation mistakes, De Morgan's law violations....

### Case 2: Alternative manifestation
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level
