---
name: performance ios autolayout perf
description: >
  Migrated review-task skill for iOS AutoLayout Performance. Use this skill whenever
  diffs may introduce performance issues on mobile, especially in Swift, Objective-C.
  Actively look for: Deeply nested constraint hierarchies, excessive
  intrinsicContentSize calls, missing StackView. and report findings with medium
  severity expectations and actionable fixes.
---

# iOS AutoLayout Performance

## Source Lineage
- Original review task: `review-tasks/performance/ios/autolayout-perf.md`
- Migrated skill artifact: `skills/review-task-performance-ios-autolayout-perf/SKILL.md`

## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Deeply nested constraint hierarchies, excessive intrinsicContentSize calls, missing StackView.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Deeply nested constraint hierarchies, excessive intrinsicContentSize calls, missing S...

### Case 2: Alternative pattern
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Issue manifests differently but same root cause.

## Counter-Examples
### Counter 1: Optimized implementation
```swift
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
