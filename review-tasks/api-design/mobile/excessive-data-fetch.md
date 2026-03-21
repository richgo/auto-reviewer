# Task: Excessive Data Fetch

## Category
api-design

## Severity
medium

## Platforms
mobile

## Languages
Swift, Kotlin

## Description
Downloading full payloads on cellular, missing pagination/field selection for mobile.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases

### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Downloading full payloads on cellular, missing pagination/field selection for mobile....

### Case 2: Alternative scenario
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Similar issue in different context.

## Counter-Examples

### Counter 1: Proper implementation
```kotlin
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Provides actionable recommendation
