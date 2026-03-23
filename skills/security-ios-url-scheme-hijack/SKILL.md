---
name: review-task-security-ios-url-scheme-hijack
description: >
  Migrated review-task skill for iOS URL Scheme Hijacking. Use this skill whenever diffs
  may introduce security issues on mobile, especially in Swift, Objective-C. Actively
  look for: Custom URL schemes without validation, universal link misconfiguration
  allowing malicious app interception. and report findings with high severity
  expectations and actionable fixes.
---

# iOS URL Scheme Hijacking

## Source Lineage
- Original review task: `review-tasks/security/ios/url-scheme-hijack.md`
- Migrated skill artifact: `skills/review-task-security-ios-url-scheme-hijack/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Custom URL schemes without validation, universal link misconfiguration allowing malicious app interception.

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
**Expected finding:** High — Custom URL schemes without validation, universal link misconfiguration allowing ... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```swift
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** High — Similar vulnerability via different code path. Apply recommended mitigations.

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
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
