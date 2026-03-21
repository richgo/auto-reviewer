# Task: Distributed Lock Issues

## Category
concurrency

## Severity
high

## Platforms
microservices

## Languages
all

## Description
Missing TTL on distributed locks (Redis/etcd), deadlock in split-brain, lock not released on failure.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases

### Case 1: Primary vulnerability
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Missing TTL on distributed locks (Redis/etcd), deadlock in split-brain, lock not released ...

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue via different approach.

## Counter-Examples

### Counter 1: Secure implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as high
- [ ] References relevant standards or guidelines
