---
name: security web client side storage
description: >
  Migrated review-task skill for Client-Side Storage Security. Use this skill whenever
  diffs may introduce security issues on web, especially in JavaScript, TypeScript.
  Actively look for: Storing tokens or secrets in localStorage, unencrypted IndexedDB,
  sensitive data in sessionStorage. and report findings with medium severity
  expectations and actionable fixes.
---

# Client-Side Storage Security

## Source Lineage
- Original review task: `review-tasks/security/web/client-side-storage.md`
- Migrated skill artifact: `skills/review-task-security-web-client-side-storage/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
Storing tokens or secrets in localStorage, unencrypted IndexedDB, sensitive data in sessionStorage.

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
**Expected finding:** Medium — Storing tokens or secrets in localStorage, unencrypted IndexedDB, sensitive data... Implement proper security controls.

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
