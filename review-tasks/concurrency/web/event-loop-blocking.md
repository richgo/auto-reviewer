# Task: Event Loop Blocking

## Category
concurrency

## Severity
high

## Platforms
web

## Languages
JavaScript, TypeScript

## Description
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
