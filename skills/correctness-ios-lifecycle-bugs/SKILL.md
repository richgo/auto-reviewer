---
name: correctness ios lifecycle bugs
description: >
  Migrated review-task skill for iOS Lifecycle Bugs. Use this skill whenever diffs may
  introduce correctness issues on mobile, especially in Swift, Objective-C. Actively
  look for: UIKit access before viewDidLoad, state corruption across scene lifecycle,
  background task expiration. and report findings with medium severity expectations and
  actionable fixes.
---

# iOS Lifecycle Bugs

## Source Lineage
- Original review task: `review-tasks/correctness/ios/lifecycle-bugs.md`
- Migrated skill artifact: `skills/review-task-correctness-ios-lifecycle-bugs/SKILL.md`

## Task Metadata
- Category: `correctness`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
UIKit access before viewDidLoad, state corruption across scene lifecycle, background task expiration.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — UIKit access before viewDidLoad, state corruption across scene lifecycle, backgr...

### Case 2: Alternative manifestation
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
