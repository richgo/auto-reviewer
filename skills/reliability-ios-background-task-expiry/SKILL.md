---
name: review-task-reliability-ios-background-task-expiry
description: >
  Migrated review-task skill for iOS Background Task Expiry. Use this skill whenever
  diffs may introduce reliability issues on mobile, especially in Swift, Objective-C.
  Actively look for: BGTask not completing before expiry, no expiration handler, data
  corruption on kill. and report findings with high severity expectations and actionable
  fixes.
---

# iOS Background Task Expiry

## Source Lineage
- Original review task: `review-tasks/reliability/ios/background-task-expiry.md`
- Migrated skill artifact: `skills/review-task-reliability-ios-background-task-expiry/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
BGTask not completing before expiry, no expiration handler, data corruption on kill.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — BGTask not completing before expiry, no expiration handler, data corruption on kill....

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
