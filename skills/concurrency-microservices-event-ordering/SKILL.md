---
name: concurrency microservices event ordering
description: >
  Event Ordering Assumptions. Use this skill whenever
  diffs may introduce concurrency issues on microservices, especially in all. Actively
  look for: Assuming ordered delivery from Kafka/RabbitMQ, missing sequence numbers or
  idempotency. and report findings with high severity expectations and actionable fixes.
---

# Event Ordering Assumptions
## Task Metadata
- Category: `concurrency`
- Severity: `high`
- Platforms: `microservices`
- Languages: `all`

## Purpose
Assuming ordered delivery from Kafka/RabbitMQ, missing sequence numbers or idempotency.

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
**Expected finding:** High — Assuming ordered delivery from Kafka/RabbitMQ, missing sequence numbers or idempotency....

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
