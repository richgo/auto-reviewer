---
name: review-task-data-microservices-schema-evolution
description: >
  Migrated review-task skill for Schema Evolution Problems. Use this skill whenever
  diffs may introduce data issues on microservices, especially in all. Actively look
  for: Breaking schema changes in shared events/topics, no Avro/protobuf evolution. and
  report findings with medium severity expectations and actionable fixes.
---

# Schema Evolution Problems

## Source Lineage
- Original review task: `review-tasks/data/microservices/schema-evolution.md`
- Migrated skill artifact: `skills/review-task-data-microservices-schema-evolution/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `medium`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Breaking schema changes in shared events/topics, no Avro/protobuf evolution.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Breaking schema changes in shared events/topics, no Avro/protobuf evolution....

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
