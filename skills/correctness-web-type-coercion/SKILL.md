---
name: correctness web type coercion
description: >
  Migrated review-task skill for Type Coercion Bugs. Use this skill whenever diffs may
  introduce correctness issues on web, especially in JavaScript, TypeScript. Actively
  look for: JavaScript loose equality (==) causing type coercion bugs, truthy/falsy
  mistakes. and report findings with medium severity expectations and actionable fixes.
---

# Type Coercion Bugs

## Source Lineage
- Original review task: `review-tasks/correctness/web/type-coercion.md`
- Migrated skill artifact: `skills/review-task-correctness-web-type-coercion/SKILL.md`

## Task Metadata
- Category: `correctness`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
JavaScript loose equality (==) causing type coercion bugs, truthy/falsy mistakes.

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
**Expected finding:** Medium — JavaScript loose equality (==) causing type coercion bugs, truthy/falsy mistakes...

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
