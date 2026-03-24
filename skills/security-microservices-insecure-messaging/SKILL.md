---
name: security microservices insecure messaging
description: >
  Insecure Messaging. Use this skill whenever diffs may
  introduce security issues on microservices, especially in all. Actively look for:
  Unencrypted message queues (Kafka, RabbitMQ), unsigned events enabling replay attacks.
  and report findings with high severity expectations and actionable fixes.
---

# Insecure Messaging
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Unencrypted message queues (Kafka, RabbitMQ), unsigned events enabling replay attacks.

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
**Expected finding:** High — Unencrypted message queues (Kafka, RabbitMQ), unsigned events enabling replay attacks....

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
