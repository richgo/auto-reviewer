---
name: performance web core web vitals
description: >
  Core Web Vitals Issues. Use this skill whenever diffs
  may introduce performance issues on web, especially in JavaScript, TypeScript, HTML.
  Actively look for: LCP/CLS/INP regressions: large images without lazy loading, layout
  shifts, long input delays. and report findings with medium severity expectations and
  actionable fixes.
---

# Core Web Vitals Issues
## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript, HTML`

## Purpose
LCP/CLS/INP regressions: large images without lazy loading, layout shifts, long input delays.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — LCP/CLS/INP regressions: large images without lazy loading, layout shifts, long input...

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
