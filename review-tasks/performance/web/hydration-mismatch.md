# Task: Hydration Mismatch

## Category
performance

## Severity
medium

## Platforms
web

## Languages
JavaScript, TypeScript

## Description
SSR/client hydration mismatches causing double renders, missing Suspense boundaries.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases

### Case 1: Problem demonstration
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — SSR/client hydration mismatches causing double renders, missing Suspense boundaries....

### Case 2: Alternative pattern
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Issue manifests differently but same root cause.

## Counter-Examples

### Counter 1: Optimized implementation
```javascript
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Uses efficient algorithms and proper resource management.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific improvements
