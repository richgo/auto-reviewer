---
name: reliability retry without backoff
description: >
  Retry Without Backoff. Use this skill whenever diffs
  may introduce reliability issues on all, especially in all. Actively look for:
  Immediate retries without exponential backoff, thundering herd on failure. and report
  findings with medium severity expectations and actionable fixes.
---

# Retry Without Backoff
## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Immediate retries without exponential backoff, thundering herd on failure.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Immediate retries without exponential backoff, thundering herd on failure....

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
