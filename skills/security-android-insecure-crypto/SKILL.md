---
name: review-task-security-android-insecure-crypto
description: >
  Migrated review-task skill for Android Insecure Cryptography. Use this skill whenever
  diffs may introduce security issues on mobile, especially in Kotlin, Java. Actively
  look for: Hardcoded encryption keys, weak algorithms (DES, ECB mode), missing Android
  Keystore usage for key storage and generation. and report findings with high severity
  expectations and actionable fixes.
---

# Android Insecure Cryptography

## Source Lineage
- Original review task: `review-tasks/security/android/insecure-crypto.md`
- Migrated skill artifact: `skills/review-task-security-android-insecure-crypto/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
Hardcoded encryption keys, weak algorithms (DES, ECB mode), missing Android Keystore usage for key storage and generation.

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
**Expected finding:** High — Hardcoded encryption keys, weak algorithms (DES, ECB mode), missing Android Keys... Implement proper security controls.

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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
