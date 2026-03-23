---
name: code quality ios deprecated api
description: >
  Migrated review-task skill for iOS Deprecated API Usage. Use this skill whenever diffs
  may introduce code-quality issues on mobile, especially in Swift, Objective-C.
  Actively look for: Using deprecated UIKit/Foundation without #available guards,
  missing replacement. and report findings with low severity expectations and actionable
  fixes.
---

# iOS Deprecated API Usage

## Source Lineage
- Original review task: `review-tasks/code-quality/ios/deprecated-api.md`
- Migrated skill artifact: `skills/review-task-code-quality-ios-deprecated-api/SKILL.md`

## Task Metadata
- Category: `code-quality`
- Severity: `low`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Using deprecated UIKit/Foundation without #available guards, missing replacement.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Using deprecated UIKit/Foundation without #available guards, missing replacement....

### Case 2: Alternative scenario
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Similar issue in different context.

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
