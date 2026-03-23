---
name: observability ios crash symbolication
description: >
  Migrated review-task skill for Crash Symbolication Missing. Use this skill whenever
  diffs may introduce observability issues on mobile, especially in Swift, Objective-C.
  Actively look for: Missing dSYM upload, bitcode symbols not preserved, unsymbolicated
  crash logs. and report findings with medium severity expectations and actionable
  fixes.
---

# Crash Symbolication Missing

## Source Lineage
- Original review task: `review-tasks/observability/ios/crash-symbolication.md`
- Migrated skill artifact: `skills/review-task-observability-ios-crash-symbolication/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Missing dSYM upload, bitcode symbols not preserved, unsymbolicated crash logs.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing dSYM upload, bitcode symbols not preserved, unsymbolicated crash logs....

### Case 2: Alternative scenario
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

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
