---
name: testing microservices contract testing
description: >
  Migrated review-task skill for Contract Testing Gaps. Use this skill whenever diffs
  may introduce testing issues on microservices, especially in all. Actively look for:
  No Pact/consumer-driven contracts, breaking API changes without cross-service
  validation. and report findings with high severity expectations and actionable fixes.
---

# Contract Testing Gaps

## Source Lineage
- Original review task: `review-tasks/testing/microservices/contract-testing.md`
- Migrated skill artifact: `skills/review-task-testing-microservices-contract-testing/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
No Pact/consumer-driven contracts, breaking API changes without cross-service validation.

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
**Expected finding:** High — No Pact/consumer-driven contracts, breaking API changes without cross-service va...

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
