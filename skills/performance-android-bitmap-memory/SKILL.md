---
name: performance android bitmap memory
description: >
  Android Bitmap Memory. Use this skill whenever diffs
  may introduce performance issues on mobile, especially in Kotlin, Java. Actively look
  for: Loading full-res bitmaps into ImageView, missing Glide/Coil downsampling, Bitmap
  not recycled. and report findings with high severity expectations and actionable
  fixes.
---

# Android Bitmap Memory
## Task Metadata
- Category: `performance`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Loading full-res bitmaps into ImageView, missing Glide/Coil downsampling, Bitmap not recycled.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Loading full-res bitmaps into ImageView, missing Glide/Coil downsampling, Bitmap not ...

### Case 2: Alternative pattern
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Issue manifests differently but same root cause.

## Counter-Examples
### Counter 1: Optimized implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Uses efficient algorithms and proper resource management.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific improvements
