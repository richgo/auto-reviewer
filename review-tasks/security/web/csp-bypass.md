# Task: Content Security Policy Bypass

## Category
security

## Severity
medium

## Platforms
web

## Languages
JavaScript, TypeScript, HTML

## Description
CSP with unsafe-inline/unsafe-eval, nonce misuse, missing object-src none, JSONP endpoints.

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
**Expected finding:** Medium — CSP with unsafe-inline/unsafe-eval, nonce misuse, missing object-src none, JSONP... Implement proper security controls.

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
