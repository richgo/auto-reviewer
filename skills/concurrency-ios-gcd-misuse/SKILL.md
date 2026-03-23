---
name: concurrency ios gcd misuse
description: >
  Migrated review-task skill for iOS GCD Misuse. Use this skill whenever diffs may
  introduce concurrency issues on mobile, especially in Swift, Objective-C. Actively
  look for: Sync dispatch on main queue causing deadlock, missing DispatchGroup
  coordination. and report findings with high severity expectations and actionable
  fixes.
---

# iOS GCD Misuse

## Source Lineage
- Original review task: `review-tasks/concurrency/ios/gcd-misuse.md`
- Migrated skill artifact: `skills/review-task-concurrency-ios-gcd-misuse/SKILL.md`

## Task Metadata
- Category: `concurrency`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Sync dispatch on main queue causing deadlock, missing DispatchGroup coordination.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases
### Case 1: Primary vulnerability
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Sync dispatch on main queue causing deadlock, missing DispatchGroup coordination....

### Case 2: Alternative pattern
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue via different approach.

## Counter-Examples
### Counter 1: Secure implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as high
- [ ] References relevant standards or guidelines

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
