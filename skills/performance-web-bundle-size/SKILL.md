---
name: review-task-performance-web-bundle-size
description: >
  Migrated review-task skill for Bundle Size Bloat. Use this skill whenever diffs may
  introduce performance issues on web, especially in JavaScript, TypeScript. Actively
  look for: Large JavaScript bundles, missing code splitting, unused dependencies in
  bundle. and report findings with low severity expectations and actionable fixes.
---

# Bundle Size Bloat

## Source Lineage
- Original review task: `review-tasks/performance/web/bundle-size.md`
- Migrated skill artifact: `skills/review-task-performance-web-bundle-size/SKILL.md`

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
