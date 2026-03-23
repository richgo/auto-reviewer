---
name: review-task-concurrency-web-event-loop-blocking
description: >
  Migrated review-task skill for Event Loop Blocking. Use this skill whenever diffs may
  introduce concurrency issues on web, especially in JavaScript, TypeScript. Actively
  look for: Long synchronous operations blocking UI, missing requestIdleCallback for
  heavy work. and report findings with high severity expectations and actionable fixes.
---

# Event Loop Blocking

## Source Lineage
- Original review task: `review-tasks/concurrency/web/event-loop-blocking.md`
- Migrated skill artifact: `skills/review-task-concurrency-web-event-loop-blocking/SKILL.md`

## Task Metadata
- Category: `concurrency`
- Severity: `high`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
Long synchronous operations blocking UI, missing requestIdleCallback for heavy work.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases
### Case 1: Primary vulnerability
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** High — Long synchronous operations blocking UI, missing requestIdleCallback for heavy work....

### Case 2: Alternative pattern
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue via different approach.

## Counter-Examples
### Counter 1: Secure implementation
```javascript
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

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
