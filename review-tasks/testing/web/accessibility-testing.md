# Task: Accessibility Testing Gaps

## Category
testing

## Severity
medium

## Platforms
web

## Languages
JavaScript, TypeScript

## Description
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
