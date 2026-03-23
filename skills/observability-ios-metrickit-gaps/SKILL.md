---
name: review-task-observability-ios-metrickit-gaps
description: >
  Migrated review-task skill for MetricKit Collection Gaps. Use this skill whenever
  diffs may introduce observability issues on mobile, especially in Swift, Objective-C.
  Actively look for: Not collecting MetricKit data, missing hang rate/disk write
  diagnostics, no custom signposts. and report findings with low severity expectations
  and actionable fixes.
---

# MetricKit Collection Gaps

## Source Lineage
- Original review task: `review-tasks/observability/ios/metrickit-gaps.md`
- Migrated skill artifact: `skills/review-task-observability-ios-metrickit-gaps/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `low`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Not collecting MetricKit data, missing hang rate/disk write diagnostics, no custom signposts.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Not collecting MetricKit data, missing hang rate/disk write diagnostics, no custom signpos...

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
