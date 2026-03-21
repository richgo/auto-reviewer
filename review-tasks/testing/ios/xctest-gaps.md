# Task: iOS XCTest Coverage Gaps

## Category
testing

## Severity
medium

## Platforms
mobile

## Languages
Swift

## Description
Missing XCUITest for critical flows, no snapshot tests, untested async expectations.

## Detection Heuristics
- Code patterns indicating the issue
- Missing validation or error handling
- API misuse or anti-patterns
- Configuration problems

## Eval Cases

### Case 1: Issue demonstration
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing XCUITest for critical flows, no snapshot tests, untested async expectati...

### Case 2: Alternative manifestation
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples

### Counter 1: Correct implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows best practices and handles edge cases properly.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding provides clear remediation steps
- [ ] Severity matches impact level
