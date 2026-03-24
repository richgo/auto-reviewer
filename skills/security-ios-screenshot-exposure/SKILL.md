---
name: security ios screenshot exposure
description: >
  iOS Screenshot Exposure. Use this skill whenever diffs
  may introduce security issues on mobile, especially in Swift, Objective-C. Actively
  look for: Sensitive screens not hidden during applicationWillResignActive, visible in
  app switcher screenshots. and report findings with low severity expectations and
  actionable fixes.
---

# iOS Screenshot Exposure
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
