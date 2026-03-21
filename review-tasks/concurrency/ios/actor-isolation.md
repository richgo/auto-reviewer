# Task: Swift Actor Isolation

## Category
concurrency

## Severity
medium

## Platforms
mobile

## Languages
Swift

## Description
Missing @MainActor, Sendable protocol violations, data races across actors.

## Detection Heuristics
- Vulnerable code patterns or missing security controls
- Configuration issues or unsafe API usage
- Missing validation or authorization checks
- Performance or reliability anti-patterns

## Eval Cases

### Case 1: Primary vulnerability
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing @MainActor, Sendable protocol violations, data races across actors....

### Case 2: Alternative pattern
```swift
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue via different approach.

## Counter-Examples

### Counter 1: Secure implementation
```swift
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Implements best practices and proper controls.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable remediation
- [ ] Severity assigned as medium
- [ ] References relevant standards or guidelines
