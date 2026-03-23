---
name: data ios coredata migration
description: >
  Migrated review-task skill for Core Data Migration Failures. Use this skill whenever
  diffs may introduce data issues on mobile, especially in Swift, Objective-C. Actively
  look for: Lightweight migration failure, missing mapping model, model version mismatch
  crash. and report findings with high severity expectations and actionable fixes.
---

# Core Data Migration Failures

## Source Lineage
- Original review task: `review-tasks/data/ios/coredata-migration.md`
- Migrated skill artifact: `skills/review-task-data-ios-coredata-migration/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Lightweight migration failure, missing mapping model, model version mismatch crash.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** High — Lightweight migration failure, missing mapping model, model version mismatch crash....

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
