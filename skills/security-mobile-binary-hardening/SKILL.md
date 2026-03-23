---
name: security mobile binary hardening
description: >
  Migrated review-task skill for Mobile Binary Hardening. Use this skill whenever diffs
  may introduce security issues on mobile, especially in Swift, Kotlin, Java. Actively
  look for: Missing ProGuard/R8 obfuscation, debug symbols in release, no root/jailbreak
  detection, anti-tamper missing. and report findings with medium severity expectations
  and actionable fixes.
---

# Mobile Binary Hardening

## Source Lineage
- Original review task: `review-tasks/security/mobile/binary-hardening.md`
- Migrated skill artifact: `skills/review-task-security-mobile-binary-hardening/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Swift, Kotlin, Java`

## Purpose
Missing ProGuard/R8 obfuscation, debug symbols in release, no root/jailbreak detection, anti-tamper missing.

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
**Expected finding:** Medium — Missing ProGuard/R8 obfuscation, debug symbols in release, no root/jailbreak det... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```kotlin
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** Medium — Similar vulnerability via different code path. Apply recommended mitigations.

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
- [ ] Severity assigned as medium

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
