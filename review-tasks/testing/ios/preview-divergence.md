# Task: SwiftUI Preview Divergence

## Category
testing

## Severity
low

## Platforms
mobile

## Languages
Swift

## Description
SwiftUI preview behavior differs from runtime, preview-only data masking production bugs.

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
**Expected finding:** Low — SwiftUI preview behavior differs from runtime, preview-only data masking product...

### Case 2: Alternative manifestation
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Low — Similar issue in different context.

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
