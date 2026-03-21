# Task: Graceful Degradation Missing

## Category
reliability

## Severity
medium

## Platforms
web, microservices

## Languages
all

## Description
Hard failures instead of fallbacks, no feature flags for degradation.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases

### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Hard failures instead of fallbacks, no feature flags for degradation....

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Issue manifests differently but same root cause.

## Counter-Examples

### Counter 1: Optimized implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Uses efficient algorithms and proper resource management.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific improvements
