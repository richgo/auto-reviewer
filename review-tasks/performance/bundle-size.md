# Task: Bundle Size Bloat

## Category
performance

## Severity
low

## Platforms
web

## Languages
JavaScript, TypeScript

## Description
Large JavaScript bundles, missing code splitting, unused dependencies in bundle.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases

### Case 1: Problem demonstration
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Large JavaScript bundles, missing code splitting, unused dependencies in bundle....

### Case 2: Alternative pattern
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Issue manifests differently but same root cause.

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
