# Task: Accessibility Issues

## Category
code-quality

## Severity
medium

## Platforms
web

## Languages
HTML, JavaScript, TypeScript

## Description
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
