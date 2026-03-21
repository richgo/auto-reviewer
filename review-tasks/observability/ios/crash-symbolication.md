# Task: Crash Symbolication Missing

## Category
observability

## Severity
medium

## Platforms
mobile

## Languages
Swift, Objective-C

## Description
Missing dSYM upload, bitcode symbols not preserved, unsymbolicated crash logs.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases

### Case 1: Issue example
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing dSYM upload, bitcode symbols not preserved, unsymbolicated crash logs....

### Case 2: Alternative scenario
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples

### Counter 1: Proper implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Provides actionable recommendation
