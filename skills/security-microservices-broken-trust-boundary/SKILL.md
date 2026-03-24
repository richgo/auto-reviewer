---
name: security microservices broken trust boundary
description: >
  Broken Trust Boundary. Use this skill whenever diffs
  may introduce security issues on microservices, especially in all. Actively look for:
  Internal services trusting external input without validation, missing API gateway
  enforcement. and report findings with critical severity expectations and actionable
  fixes.
---

# Broken Trust Boundary
## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Internal services trusting external input without validation, missing API gateway enforcement.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases
### Case 1: Primary vulnerability
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Critical — Internal services trusting external input without validation, missing API gateway enforcem...

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Critical — Similar issue via different approach.

## Counter-Examples
### Counter 1: Secure implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as critical
- [ ] References relevant standards or guidelines
