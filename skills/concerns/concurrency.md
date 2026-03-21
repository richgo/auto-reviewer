---
name: concurrency
description: >
  Detect concurrency bugs: race conditions, deadlocks, async/await misuse, thread-unsafe collections,
  and livelocks. Trigger when reviewing multi-threaded code, async operations, shared mutable state,
  lock usage, coroutines, GCD/dispatch queues, or parallel data structures.
---

# Security & Correctness Review: Concurrency Issues

## Purpose
Review code for concurrency bugs that cause data corruption, crashes, deadlocks, or performance degradation in multi-threaded or async environments.

## Scope
Five universal concurrency vulnerability classes plus platform-specific patterns:
1. **Race Conditions** — unsynchronized access to shared mutable state
2. **Deadlocks** — circular lock dependencies causing thread stalls
3. **Async Misuse** — incorrect async/await usage, unhandled promises
4. **Thread-Unsafe Collections** — concurrent modification of non-thread-safe data structures
5. **Livelock** — threads continuously changing state in response to each other

**Platform-specific:**
- **Android:** Main thread blocking, coroutine misuse, Handler/Looper leaks
- **iOS:** Main thread blocking, GCD misuse, actor isolation violations
- **Web:** Event loop blocking, Web Worker postMessage overhead
- **Microservices:** Distributed locks without TTL, event ordering assumptions, thundering herd

## Detection Strategy

### Universal Red Flags
- **Shared mutable state** without locks/atomics
- **Nested locks** (potential deadlock)
- **Blocking operations** in async context or UI thread
- **`await` inside loops** (sequential instead of parallel)
- **Unhandled promise rejections**
- **Thread-unsafe collections** (`ArrayList`, `HashMap`) used concurrently

### High-Risk Patterns

**Race Conditions:**
- `counter++` on shared variable without lock
- Check-then-act without atomicity: `if (!exists) { create() }`
- Multiple threads writing to same file/DB record

**Deadlocks:**
- Lock A → Lock B in thread 1, Lock B → Lock A in thread 2
- Nested `synchronized` blocks with different order
- `await` inside lock (holding lock across async boundary)

**Async Misuse:**
- `Promise` not awaited (fire-and-forget)
- `await` in loop: `for (x of items) { await process(x) }`
- Wrong async context (I/O on UI thread)

**Thread-Unsafe Collections:**
- `ArrayList.add()` from multiple threads
- `HashMap.put()` without `ConcurrentHashMap` or lock

**Livelock:**
- Threads continuously retrying with same conditions
- Collision avoidance algorithms without randomized backoff

## Platform-Specific Guidance

### Android
- **Key anti-patterns:** Network/DB on main thread, `GlobalScope.launch`, leaked Handler
- **Detection:** `StrictMode` violations, `Dispatchers.Main` for I/O, missing `viewModelScope`
- **Safe patterns:** `Dispatchers.IO` for I/O, `viewModelScope`/`lifecycleScope`, `Flow` for streams

### iOS
- **Key anti-patterns:** Sync network on main queue, `DispatchQueue.main.sync` from main, actor race
- **Detection:** UI updates from background thread, missing `@MainActor`, `Sendable` violations
- **Safe patterns:** `DispatchQueue.global()` for I/O, `@MainActor` for UI updates, Swift actors

### Web
- **Key anti-patterns:** Long sync operations blocking event loop, SharedArrayBuffer without Atomics
- **Detection:** Slow render times, unresponsive UI, missing `requestIdleCallback`
- **Safe patterns:** Web Workers for heavy compute, `Promise.all()` for parallelism

### Microservices
- **Key anti-patterns:** Distributed lock without TTL, assuming ordered delivery, synchronized retries
- **Detection:** Split-brain scenarios, duplicate processing, cache stampede
- **Safe patterns:** Redis locks with TTL, idempotency keys, jittered backoff

## Review Instructions

### Step 1: Identify Shared State
Find all mutable data accessed by multiple threads/coroutines:
- Instance variables in multi-threaded classes
- Global variables
- Database records written by concurrent requests
- Cache entries

### Step 2: Check Synchronization
For each shared mutable variable:
1. **Protected by lock?** (`synchronized`, `Mutex`, `Lock`)
2. **Atomic operations?** (`AtomicInteger`, `std::atomic`)
3. **Immutable?** (Prefer immutable data structures)

### Step 3: Detect Deadlock Risks
- Map all lock acquisition orders
- Check for cycles (A→B, B→A)
- Look for `await` or blocking calls inside locks

### Step 4: Review Async Patterns
- **UI/main thread:** No blocking I/O
- **Parallelization:** Use `Promise.all()`, `asyncio.gather()`, not sequential awaits
- **Error handling:** All promises have `.catch()` or try/catch

### Step 5: Validate Collection Usage
- **Concurrent access:** Use `ConcurrentHashMap`, `CopyOnWriteArrayList`, or explicit locks
- **Iteration:** Lock during iteration or use snapshot copy

### Step 6: Platform-Specific Checks
- **Android:** Check dispatcher usage, `StrictMode` compliance
- **iOS:** Check queue usage, actor isolation
- **Web:** Check event loop blocking
- **Microservices:** Check distributed lock TTL, idempotency

### Step 7: Report Findings
For each issue:
- **Severity:** High (race condition, deadlock), Medium (async misuse, thread-unsafe collection)
- **Location:** File, line, variable/method name
- **Description:** Concurrency hazard with scenario
- **Fix:** Specific remediation (lock, atomic, actor, dispatcher change)

## Examples

### ✅ SAFE: Atomic Counter
```python
from threading import Lock
lock = Lock()
with lock:
    counter += 1
```

### ❌ UNSAFE: Race Condition
```python
counter += 1  # Multiple threads
```
**Finding:** High — Race condition on shared `counter`. Use lock or `threading.atomic`.

### ✅ SAFE: Parallel Async (Node.js)
```javascript
await Promise.all(items.map(item => processItem(item)));
```

### ❌ UNSAFE: Sequential Async
```javascript
for (const item of items) {
  await processItem(item);  // Serial, not parallel
}
```
**Finding:** Medium — Sequential async in loop. Use `Promise.all()` for parallelism.

### ✅ SAFE: Android Coroutine (Kotlin)
```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val data = fetchData()
    withContext(Dispatchers.Main) {
        textView.text = data
    }
}
```

### ❌ UNSAFE: Main Thread Blocking (Kotlin)
```kotlin
viewModelScope.launch(Dispatchers.Main) {
    val data = fetchData()  // Network on main thread
    textView.text = data
}
```
**Finding:** High — Network I/O on main thread causes ANR. Use `Dispatchers.IO`.

## Related Review Tasks
- `review-tasks/concurrency/race-condition.md`
- `review-tasks/concurrency/deadlock.md`
- `review-tasks/concurrency/async-misuse.md`
- `review-tasks/concurrency/thread-unsafe-collection.md`
- `review-tasks/concurrency/livelock.md`
- Platform-specific tasks in `android/`, `ios/`, `web/`, `microservices/`

## Quick Checklist
- [ ] Shared mutable state protected by locks or atomics
- [ ] No nested locks with potential circular dependencies
- [ ] No blocking I/O on UI/main thread
- [ ] Async operations parallelized where possible
- [ ] Thread-safe collections used for concurrent access
- [ ] Distributed locks have TTL (microservices)
- [ ] Correct dispatcher/queue for operation type (Android/iOS)
