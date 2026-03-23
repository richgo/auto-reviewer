---
name: correctness microservices eventual consistency
description: >
  Migrated review-task skill for Eventual Consistency Issues. Use this skill whenever
  diffs may introduce correctness issues on microservices, especially in all. Actively
  look for: Reading stale data across services, missing saga compensation logic, split-
  brain state. and report findings with high severity expectations and actionable fixes.
---

# Eventual Consistency Issues

## Source Lineage
- Original review task: `review-tasks/correctness/microservices/eventual-consistency.md`
- Migrated skill artifact: `skills/review-task-correctness-microservices-eventual-consistency/SKILL.md`

## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Reading stale data across services, missing saga compensation logic, split-brain state.

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
**Expected finding:** High — Reading stale data across services, missing saga compensation logic, split-brain...

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
