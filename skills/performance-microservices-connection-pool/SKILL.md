---
name: performance microservices connection pool
description: >
  Connection Pool Exhaustion. Use this skill whenever
  diffs may introduce performance issues on microservices, especially in all. Actively
  look for: Unbounded connections, pool exhaustion under load, missing connection reuse.
  and report findings with high severity expectations and actionable fixes.
---

# Connection Pool Exhaustion
## Task Metadata
- Category: `performance`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Unbounded connections, pool exhaustion under load, missing connection reuse.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Unbounded connections, pool exhaustion under load, missing connection reuse....

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Issue manifests differently but same root cause.

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
