---
name: review-task-testing-ios-preview-divergence
description: >
  Migrated review-task skill for SwiftUI Preview Divergence. Use this skill whenever
  diffs may introduce testing issues on mobile, especially in Swift. Actively look for:
  SwiftUI preview behavior differs from runtime, preview-only data masking production
  bugs. and report findings with low severity expectations and actionable fixes.
---

# SwiftUI Preview Divergence

## Source Lineage
- Original review task: `review-tasks/testing/ios/preview-divergence.md`
- Migrated skill artifact: `skills/review-task-testing-ios-preview-divergence/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `low`
- Platforms: `mobile`
- Languages: `Swift`

## Purpose
SwiftUI preview behavior differs from runtime, preview-only data masking production bugs.

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
**Expected finding:** Low — SwiftUI preview behavior differs from runtime, preview-only data masking product...

### Case 2: Alternative manifestation
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Similar issue in different context.

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
