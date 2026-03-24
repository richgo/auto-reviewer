---
name: security ios keychain misuse
description: >
  iOS Keychain Misuse. Use this skill whenever diffs may
  introduce security issues on mobile, especially in Swift, Objective-C. Actively look
  for: Wrong Keychain accessibility class (kSecAttrAccessibleAlways) or missing
  kSecAttrAccessControl flags. and report findings with medium severity expectations and
  actionable fixes.
---

# iOS Keychain Misuse
## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Objective-C`

## Purpose
Wrong Keychain accessibility class (kSecAttrAccessibleAlways) or missing kSecAttrAccessControl flags.

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
**Expected finding:** Medium — Wrong Keychain accessibility class (kSecAttrAccessibleAlways) or missing kSecAtt... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```swift
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** Medium — Similar vulnerability via different code path. Apply recommended mitigations.

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
- [ ] Severity assigned as medium
