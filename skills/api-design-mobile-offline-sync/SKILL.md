---
name: api design mobile offline sync
description: >
  Mobile Offline Sync Issues. Use this skill whenever
  diffs may introduce api-design issues on mobile, especially in Swift, Kotlin. Actively
  look for: No conflict resolution for offline edits, missing CRDT/last-write-wins
  strategy, sync race conditions. and report findings with high severity expectations
  and actionable fixes.
---

# Mobile Offline Sync Issues
## Task Metadata
- Category: `api-design`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Swift, Kotlin`

## Purpose
No conflict resolution for offline edits, missing CRDT/last-write-wins strategy, sync race conditions.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — No conflict resolution for offline edits, missing CRDT/last-write-wins strategy, sync race...

### Case 2: Alternative scenario
```kotlin
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

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
