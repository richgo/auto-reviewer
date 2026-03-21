# Task: Web E2E Test Gaps

## Category
testing

## Severity
medium

## Platforms
web

## Languages
JavaScript, TypeScript

## Description
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
