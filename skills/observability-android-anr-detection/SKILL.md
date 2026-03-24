---
name: observability android anr detection
description: >
  ANR Detection Missing. Use this skill whenever diffs
  may introduce observability issues on mobile, especially in Kotlin, Java. Actively
  look for: No ANR monitoring, missing StrictMode in debug, no main thread watchdog. and
  report findings with medium severity expectations and actionable fixes.
---

# ANR Detection Missing
## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
No ANR monitoring, missing StrictMode in debug, no main thread watchdog.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** Medium — No ANR monitoring, missing StrictMode in debug, no main thread watchdog....

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
