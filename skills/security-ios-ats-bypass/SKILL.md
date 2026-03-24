---
name: security ios ats bypass
description: >
  iOS ATS Bypass. Use this skill whenever diffs may
  introduce security issues on mobile, especially in Swift, Objective-C. Actively look
  for: App Transport Security disabled via NSAllowsArbitraryLoads or NSExceptionDomains
  allowing unencrypted HTTP. and report findings with high severity expectations and
  actionable fixes.
---

# iOS ATS Bypass
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
App Transport Security disabled via NSAllowsArbitraryLoads or NSExceptionDomains allowing unencrypted HTTP.

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
**Expected finding:** High — App Transport Security disabled via NSAllowsArbitraryLoads or NSExceptionDomains... Implement proper security controls.

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
