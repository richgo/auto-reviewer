---
name: security android network security
description: >
  Android Network Security Config. Use this skill
  whenever diffs may introduce security issues on mobile, especially in Kotlin, Java,
  XML. Actively look for: Missing network_security_config.xml, cleartext traffic
  allowed, certificate validation bypass, missing certificate pinning. and report
  findings with high severity expectations and actionable fixes.
---

# Android Network Security Config
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java, XML`

## Purpose
Missing network_security_config.xml, cleartext traffic allowed, certificate validation bypass, missing certificate pinning.

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
**Expected finding:** High — Missing network_security_config.xml, cleartext traffic allowed, certificate vali... Implement proper security controls.

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
