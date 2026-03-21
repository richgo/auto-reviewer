# Task: Correlation ID Missing

## Category
observability

## Severity
high

## Platforms
microservices

## Languages
all

## Description
Missing trace/correlation ID propagation across calls, broken distributed trace.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases

### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Missing trace/correlation ID propagation across calls, broken distributed trace....

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
