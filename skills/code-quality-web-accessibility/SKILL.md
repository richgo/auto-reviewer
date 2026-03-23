---
name: code quality web accessibility
description: >
  Migrated review-task skill for Accessibility Issues. Use this skill whenever diffs may
  introduce code-quality issues on web, especially in HTML, JavaScript, TypeScript.
  Actively look for: Missing ARIA labels, insufficient color contrast, no keyboard
  navigation support. and report findings with medium severity expectations and
  actionable fixes.
---

# Accessibility Issues

## Source Lineage
- Original review task: `review-tasks/code-quality/web/accessibility.md`
- Migrated skill artifact: `skills/review-task-code-quality-web-accessibility/SKILL.md`

## Task Metadata
- Category: `code-quality`
- Severity: `medium`
- Platforms: `web`
- Languages: `HTML, JavaScript, TypeScript`

## Purpose
Missing ARIA labels, insufficient color contrast, no keyboard navigation support.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing ARIA labels, insufficient color contrast, no keyboard navigation support....

### Case 2: Alternative scenario
```javascript
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples
### Counter 1: Proper implementation
```javascript
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Provides actionable recommendation

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
