---
name: review-task-security-ios-screenshot-exposure
description: >
  Migrated review-task skill for iOS Screenshot Exposure. Use this skill whenever diffs
  may introduce security issues on mobile, especially in Swift, Objective-C. Actively
  look for: Sensitive screens not hidden during applicationWillResignActive, visible in
  app switcher screenshots. and report findings with low severity expectations and
  actionable fixes.
---

# iOS Screenshot Exposure

## Source Lineage
- Original review task: `review-tasks/security/ios/screenshot-exposure.md`
- Migrated skill artifact: `skills/review-task-security-ios-screenshot-exposure/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `low`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Sensitive screens not hidden during applicationWillResignActive, visible in app switcher screenshots.

## Detection Heuristics
- Presence of vulnerable patterns in code diffs
- Missing security controls or validation
- Use of deprecated or unsafe APIs
- Configuration issues enabling exploitation

## Eval Cases
### Case 1: Basic vulnerability pattern
```swift
// BUGGY CODE — should be detected
// Example demonstrating the vulnerability
```
**Expected finding:** Low — Sensitive screens not hidden during applicationWillResignActive, visible in app ... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```swift
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** Low — Similar vulnerability via different code path. Apply recommended mitigations.

## Counter-Examples
### Counter 1: Secure implementation
```swift
// CORRECT CODE — should NOT be flagged
// Demonstrates proper security controls
```
**Why it's correct:** Implements recommended security practices and validation.

## Binary Eval Assertions
- [ ] Detects vulnerability in eval case 1
- [ ] Detects vulnerability in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes file and line reference
- [ ] Finding includes actionable fix suggestion
- [ ] Severity assigned as low

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
