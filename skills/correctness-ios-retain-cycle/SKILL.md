---
name: correctness ios retain cycle
description: >
  Migrated review-task skill for iOS Retain Cycles. Use this skill whenever diffs may
  introduce correctness issues on mobile, especially in Swift, Objective-C. Actively
  look for: Strong reference cycles in closures (missing [weak self]), delegates not
  weak, NotificationCenter leaks. and report findings with high severity expectations
  and actionable fixes.
---

# iOS Retain Cycles

## Source Lineage
- Original review task: `review-tasks/correctness/ios/retain-cycle.md`
- Migrated skill artifact: `skills/review-task-correctness-ios-retain-cycle/SKILL.md`

## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Strong reference cycles in closures (missing [weak self]), delegates not weak, NotificationCenter leaks.

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
**Expected finding:** High — Strong reference cycles in closures (missing [weak self]), delegates not weak, N...

### Case 2: Alternative manifestation
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

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
