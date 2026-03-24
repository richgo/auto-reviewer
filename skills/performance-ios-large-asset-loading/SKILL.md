---
name: performance ios large asset loading
description: >
  iOS Large Asset Loading. Use this skill whenever diffs
  may introduce performance issues on mobile, especially in Swift, Objective-C. Actively
  look for: Loading full-res images without downsampling, missing NSCache, no
  progressive loading. and report findings with medium severity expectations and
  actionable fixes.
---

# iOS Large Asset Loading
## Task Metadata
- Category: `performance`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Loading full-res images without downsampling, missing NSCache, no progressive loading.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Loading full-res images without downsampling, missing NSCache, no progressive loading...

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
