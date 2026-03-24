---
name: code quality android accessibility
description: >
  Android Accessibility. Use this skill whenever diffs
  may introduce code-quality issues on mobile, especially in Kotlin, Java, XML. Actively
  look for: Missing contentDescription, touch targets <48dp, no TalkBack support,
  missing importantForAccessibility. and report findings with medium severity
  expectations and actionable fixes.
---

# Android Accessibility
## Task Metadata
- Category: `code-quality`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java, XML`

## Purpose
Missing contentDescription, touch targets <48dp, no TalkBack support, missing importantForAccessibility.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — Missing contentDescription, touch targets <48dp, no TalkBack support, missing importantFor...

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
