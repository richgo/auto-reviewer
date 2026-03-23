---
name: api design microservices api contract
description: >
  Migrated review-task skill for API Contract Issues. Use this skill whenever diffs may
  introduce api-design issues on microservices, especially in all. Actively look for: No
  OpenAPI/protobuf schema, breaking changes without version bump, missing deprecation
  notices. and report findings with high severity expectations and actionable fixes.
---

# API Contract Issues

## Source Lineage
- Original review task: `review-tasks/api-design/microservices/api-contract.md`
- Migrated skill artifact: `skills/review-task-api-design-microservices-api-contract/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
No OpenAPI/protobuf schema, breaking changes without version bump, missing deprecation notices.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — No OpenAPI/protobuf schema, breaking changes without version bump, missing deprecation not...

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
