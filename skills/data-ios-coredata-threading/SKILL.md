---
name: data ios coredata threading
description: >
  Core Data Threading Issues. Use this skill whenever
  diffs may introduce data issues on mobile, especially in Swift, Objective-C. Actively
  look for: NSManagedObject accessed across threads, missing performBlock, context merge
  conflicts. and report findings with high severity expectations and actionable fixes.
---

# Core Data Threading Issues
## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
NSManagedObject accessed across threads, missing performBlock, context merge conflicts.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — NSManagedObject accessed across threads, missing performBlock, context merge conflicts....

### Case 2: Alternative scenario
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

## Counter-Examples
### Counter 1: Proper implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Provides actionable recommendation
