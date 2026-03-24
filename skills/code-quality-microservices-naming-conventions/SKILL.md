---
name: code quality microservices naming conventions
description: >
  Naming Convention Inconsistency. Use this skill
  whenever diffs may introduce code-quality issues on microservices, especially in all.
  Actively look for: Inconsistent naming across services (snake_case vs camelCase),
  mismatched HTTP methods. and report findings with low severity expectations and
  actionable fixes.
---

# Naming Convention Inconsistency
## Task Metadata
- Category: `code-quality`
- Severity: `low`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Inconsistent naming across services (snake_case vs camelCase), mismatched HTTP methods.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Inconsistent naming across services (snake_case vs camelCase), mismatched HTTP methods....

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
