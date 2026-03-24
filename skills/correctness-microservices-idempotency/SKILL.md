---
name: correctness microservices idempotency
description: >
  Missing Idempotency. Use this skill whenever diffs may
  introduce correctness issues on microservices, especially in all. Actively look for:
  Non-idempotent message handlers, duplicate processing, missing idempotency keys. and
  report findings with high severity expectations and actionable fixes.
---

# Missing Idempotency
## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Non-idempotent message handlers, duplicate processing, missing idempotency keys.

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
**Expected finding:** High — Non-idempotent message handlers, duplicate processing, missing idempotency keys....

### Case 2: Alternative manifestation
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

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
