---
name: security mobile cert pinning
description: >
  Mobile Certificate Pinning. Use this skill whenever
  diffs may introduce security issues on mobile, especially in Swift, Kotlin,
  Objective-C, Java. Actively look for: Missing certificate or public key pinning for
  sensitive API endpoints enabling MitM attacks. and report findings with high severity
  expectations and actionable fixes.
---

# Mobile Certificate Pinning
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Kotlin, Objective-C, Java`

## Purpose
Missing certificate or public key pinning for sensitive API endpoints enabling MitM attacks.

## Detection Heuristics
- Presence of vulnerable patterns in code diffs
- Missing security controls or validation
- Use of deprecated or unsafe APIs
- Configuration issues enabling exploitation

## Eval Cases
### Case 1: Basic vulnerability pattern
```kotlin
// BUGGY CODE — should be detected
// Example demonstrating the vulnerability
```
**Expected finding:** High — Missing certificate or public key pinning for sensitive API endpoints enabling M... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```kotlin
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** High — Similar vulnerability via different code path. Apply recommended mitigations.

## Counter-Examples
### Counter 1: Secure implementation
```kotlin
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
