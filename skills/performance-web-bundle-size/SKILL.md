---
name: performance web bundle size
description: >
  Bundle Size Bloat. Use this skill whenever diffs may
  introduce performance issues on web, especially in JavaScript, TypeScript. Actively
  look for: Large JavaScript bundles, missing code splitting, unused dependencies in
  bundle. and report findings with low severity expectations and actionable fixes.
---

# Bundle Size Bloat
## Task Metadata
- Category: `performance`
- Severity: `low`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
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
