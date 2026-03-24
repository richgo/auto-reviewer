---
name: performance web unnecessary rerender
description: >
  Unnecessary Re-renders. Use this skill whenever diffs
  may introduce performance issues on web, especially in JavaScript, TypeScript.
  Actively look for: React/Vue components re-rendering unnecessarily, missing
  memoization, prop drilling. and report findings with medium severity expectations and
  actionable fixes.
---

# Unnecessary Re-renders
## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
React/Vue components re-rendering unnecessarily, missing memoization, prop drilling.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — React/Vue components re-rendering unnecessarily, missing memoization, prop drilling....

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
