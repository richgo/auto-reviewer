---
name: security web html injection
description: >
  Migrated review-task skill for HTML Injection. Use this skill whenever diffs may
  introduce security issues on web, especially in all. Actively look for: User content
  injected into meta tags, link href, form action enabling phishing or open redirect.
  and report findings with medium severity expectations and actionable fixes.
---

# HTML Injection

## Source Lineage
- Original review task: `review-tasks/security/web/html-injection.md`
- Migrated skill artifact: `skills/review-task-security-web-html-injection/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web`
- Languages: `all`

## Purpose
User content injected into meta tags, link href, form action enabling phishing or open redirect.

## Detection Heuristics
- Presence of vulnerable patterns in code diffs
- Missing security controls or validation
- Use of deprecated or unsafe APIs
- Configuration issues enabling exploitation

## Eval Cases
### Case 1: Basic vulnerability pattern
```java
// BUGGY CODE — should be detected
// Example demonstrating the vulnerability
```
**Expected finding:** Medium — User content injected into meta tags, link href, form action enabling phishing o... Implement proper security controls.

### Case 2: Alternative vulnerability vector
```java
// BUGGY CODE — should be detected  
// Alternative pattern showing same issue
```
**Expected finding:** Medium — Similar vulnerability via different code path. Apply recommended mitigations.

## Counter-Examples
### Counter 1: Secure implementation
```java
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
