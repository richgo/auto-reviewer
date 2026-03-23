---
name: testing web e2e gaps
description: >
  Migrated review-task skill for Web E2E Test Gaps. Use this skill whenever diffs may
  introduce testing issues on web, especially in JavaScript, TypeScript. Actively look
  for: Critical user flows without E2E tests (Playwright/Cypress), no visual regression
  testing. and report findings with medium severity expectations and actionable fixes.
---

# Web E2E Test Gaps

## Source Lineage
- Original review task: `review-tasks/testing/web/e2e-gaps.md`
- Migrated skill artifact: `skills/review-task-testing-web-e2e-gaps/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
Critical user flows without E2E tests (Playwright/Cypress), no visual regression testing.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases
### Case 1: Issue demonstration
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Critical user flows without E2E tests (Playwright/Cypress), no visual regression...

### Case 2: Alternative manifestation
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Correct implementation
```javascript
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
