---
name: performance ios main thread work
description: >
  iOS Main Thread Work. Use this skill whenever diffs may
  introduce performance issues on mobile, especially in Swift, Objective-C. Actively
  look for: Image decoding/JSON parsing on main, UITableView cell height recalculation,
  Core Data on main. and report findings with high severity expectations and actionable
  fixes.
---

# iOS Main Thread Work
## Task Metadata
- Category: `performance`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Image decoding/JSON parsing on main, UITableView cell height recalculation, Core Data on main.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Image decoding/JSON parsing on main, UITableView cell height recalculation, Core Data...

### Case 2: Alternative pattern
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Issue manifests differently but same root cause.

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
