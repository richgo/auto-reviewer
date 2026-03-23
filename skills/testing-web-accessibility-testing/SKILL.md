---
name: review-task-testing-web-accessibility-testing
description: >
  Migrated review-task skill for Accessibility Testing Gaps. Use this skill whenever
  diffs may introduce testing issues on web, especially in JavaScript, TypeScript.
  Actively look for: Missing axe/WAVE assertions, no keyboard navigation tests, ARIA
  coverage gaps. and report findings with medium severity expectations and actionable
  fixes.
---

# Accessibility Testing Gaps

## Source Lineage
- Original review task: `review-tasks/testing/web/accessibility-testing.md`
- Migrated skill artifact: `skills/review-task-testing-web-accessibility-testing/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
Missing axe/WAVE assertions, no keyboard navigation tests, ARIA coverage gaps.

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
**Expected finding:** Medium — Missing axe/WAVE assertions, no keyboard navigation tests, ARIA coverage gaps....

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
