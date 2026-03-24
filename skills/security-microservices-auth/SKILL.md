---
name: security microservices auth
description: >
  Microservices Authentication. Use this skill whenever
  diffs may introduce security issues on microservices, especially in all. Actively look
  for: Missing service-to-service authentication, relying on network isolation, shared
  secrets across services. and report findings with high severity expectations and
  actionable fixes.
---

# Microservices Authentication
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Missing service-to-service authentication, relying on network isolation, shared secrets across services.

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
**Expected finding:** High — Missing service-to-service authentication, relying on network isolation, shared secrets ac...

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue via different approach.

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
- [ ] Severity assigned as high
- [ ] References relevant standards or guidelines
