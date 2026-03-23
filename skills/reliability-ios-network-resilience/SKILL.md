---
name: review-task-reliability-ios-network-resilience
description: >
  Migrated review-task skill for iOS Network Resilience. Use this skill whenever diffs
  may introduce reliability issues on mobile, especially in Swift, Objective-C. Actively
  look for: No offline handling, URLSession not for background downloads, missing
  NWPathMonitor. and report findings with medium severity expectations and actionable
  fixes.
---

# iOS Network Resilience

## Source Lineage
- Original review task: `review-tasks/reliability/ios/network-resilience.md`
- Migrated skill artifact: `skills/review-task-reliability-ios-network-resilience/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
No offline handling, URLSession not for background downloads, missing NWPathMonitor.

## Detection Heuristics
- Identifying patterns that indicate the issue
- Missing optimizations or controls
- Anti-patterns or inefficient implementations

## Eval Cases
### Case 1: Problem demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No offline handling, URLSession not for background downloads, missing NWPathMonitor....

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
