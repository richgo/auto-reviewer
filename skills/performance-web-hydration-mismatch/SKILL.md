---
name: performance web hydration mismatch
description: >
  Migrated review-task skill for Hydration Mismatch. Use this skill whenever diffs may
  introduce performance issues on web, especially in JavaScript, TypeScript. Actively
  look for: SSR/client hydration mismatches causing double renders, missing Suspense
  boundaries. and report findings with medium severity expectations and actionable
  fixes.
---

# Hydration Mismatch

## Source Lineage
- Original review task: `review-tasks/performance/web/hydration-mismatch.md`
- Migrated skill artifact: `skills/review-task-performance-web-hydration-mismatch/SKILL.md`

## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
