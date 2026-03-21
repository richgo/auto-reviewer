# Task: Schema Evolution Problems

## Category
data

## Severity
medium

## Platforms
microservices

## Languages
all

## Description
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
