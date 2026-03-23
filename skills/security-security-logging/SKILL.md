---
name: review-task-security-security-logging
description: >
  Migrated review-task skill for Security Logging Gaps. Use this skill whenever diffs
  may introduce security issues on all, especially in all. Actively look for: Missing
  logs for security events: auth failures, privilege changes, data access, admin
  actions. and report findings with medium severity expectations and actionable fixes.
---

# Security Logging Gaps

## Source Lineage
- Original review task: `review-tasks/security/security-logging.md`
- Migrated skill artifact: `skills/review-task-security-security-logging/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Missing logs for security events: auth failures, privilege changes, data access, admin actions.

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
**Expected finding:** Medium — Missing logs for security events: auth failures, privilege changes, data access, admin act...

### Case 2: Alternative pattern
```java
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue via different approach.

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
- [ ] Severity assigned as medium
- [ ] References relevant standards or guidelines

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
