---
name: concurrency deadlock
description: >
  Migrated review-task skill for Deadlock. Use this skill whenever diffs may introduce
  concurrency issues on all, especially in java, python, go, csharp, cpp, rust. Actively
  look for: Two or more threads each holding a lock while waiting for a lock held by the
  other, causing... and report findings with high severity expectations and actionable
  fixes.
---

# Deadlock

## Source Lineage
- Original review task: `review-tasks/concurrency/deadlock.md`
- Migrated skill artifact: `skills/review-task-concurrency-deadlock/SKILL.md`

## Task Metadata
- Category: `concurrency`
- Severity: `high`
- Platforms: `all`
- Languages: `java, python, go, csharp, cpp, rust`

## Purpose
Two or more threads each holding a lock while waiting for a lock held by the other, causing permanent hang. Also includes self-deadlock (re-acquiring non-reentrant lock).

## Detection Heuristics
- Multiple locks acquired in different orders across code paths
- Nested `synchronized` blocks or `lock.acquire()` on different objects
- Holding a lock while calling external/callback code that may acquire another lock
- Channel operations in Go that can block indefinitely
- Database transactions that lock rows in inconsistent order

## Eval Cases
### Case 1: Lock ordering violation
```java
// Thread 1 path
synchronized (lockA) {
    synchronized (lockB) {
        transferFunds(a, b);
    }
}

// Thread 2 path  
synchronized (lockB) {
    synchronized (lockA) {
        transferFunds(b, a);
    }
}
```
**Expected finding:** High — Deadlock risk. Thread 1 holds lockA and waits for lockB, while Thread 2 holds lockB and waits for lockA. Enforce consistent lock ordering (always acquire lockA before lockB).

### Case 2: Go channel deadlock
```go
func process() {
    ch := make(chan int)
    ch <- 42  // blocks forever — no receiver yet
    val := <-ch
    fmt.Println(val)
}
```
**Expected finding:** High — Deadlock. Unbuffered channel send blocks because receiver hasn't started. Use buffered channel or separate goroutine.

## Counter-Examples
### Counter 1: Consistent lock ordering
```java
// Both paths acquire locks in same order
synchronized (lockA) {
    synchronized (lockB) {
        transferFunds(a, b);
    }
}
```
**Why it's correct:** Consistent ordering prevents circular wait.

## Binary Eval Assertions
- [ ] Detects lock ordering violation in eval case 1
- [ ] Detects channel deadlock in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the circular wait pattern
- [ ] Finding suggests fix (ordering, buffering)
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
