---
name: reliability
description: >
  Detect reliability issues: inadequate error handling, missing resource cleanup, improper timeout
  handling, lack of graceful degradation, and retry without backoff. Trigger when reviewing error
  handling code, resource management (files, connections, locks), timeout configurations, fallback
  logic, or retry mechanisms. Critical for production stability and user experience.
---

# Reliability Review

## Purpose
Review code for reliability issues that cause crashes, resource leaks, cascading failures, or poor user experience: error handling gaps, missing resource cleanup, timeout misconfigurations, lack of graceful degradation, and naive retry strategies.

## Scope
1. **Error Handling** — uncaught exceptions, swallowed errors, missing validation, panic without recovery
2. **Resource Cleanup** — leaked file handles, unclosed connections, unreleased locks, memory leaks
3. **Timeout Handling** — infinite waits, missing timeouts, timeout too short/long
4. **Graceful Degradation** — hard failures when soft failures acceptable, no fallback logic
5. **Retry Without Backoff** — immediate retries, no exponential backoff, missing jitter, retry storms

## Detection Strategy

### 1. Error Handling Red Flags
- **Bare except/catch** catching all exceptions including system exits
- **Empty catch blocks** (`catch (e) {}`)
- **Swallowed exceptions** (logged but not propagated)
- **No validation** before operations
- **Panic/crash on expected errors** (network failure, file not found)

**High-risk patterns:**
```python
# ❌ UNSAFE
try:
    risky_operation()
except:  # Catches KeyboardInterrupt, SystemExit
    pass  # Swallowed
```

### 2. Resource Cleanup Red Flags
- **Files opened without** `with` statement or `finally` block
- **Database connections not closed** on error path
- **Locks acquired but not released** in all paths
- **No defer/finally** for cleanup in Go/Java
- **Memory leaks** from circular references, unclosed handlers

**High-risk patterns:**
```python
# ❌ UNSAFE
f = open('file.txt')
data = f.read()
process(data)
f.close()  # Not called if process() raises
```

### 3. Timeout Handling Red Flags
- **No timeout** on network calls
- **Infinite wait** on locks/semaphores
- **Timeout hardcoded** without configuration
- **Timeout shorter than** expected latency (flaky)
- **No timeout context propagation** (Go, distributed systems)

**High-risk patterns:**
```python
# ❌ UNSAFE
response = requests.get(url)  # No timeout, can hang forever
lock.acquire()  # Blocks forever if deadlock
```

### 4. Graceful Degradation Red Flags
- **Hard failure on non-critical dependency** (recommendation service down → entire page fails)
- **No fallback** for cache miss
- **Synchronous call to optional feature** (blocks on failure)
- **Circuit breaker missing** for flaky services

**High-risk patterns:**
```python
# ❌ UNSAFE
recommendations = fetch_recommendations()  # Fails entire page if service down
render_page(recommendations)
```

### 5. Retry Without Backoff Red Flags
- **Immediate retry** in loop without delay
- **No exponential backoff**
- **No jitter** (synchronized retries cause thundering herd)
- **Infinite retries** without max attempts
- **Retrying non-idempotent operations**

**High-risk patterns:**
```python
# ❌ UNSAFE
while True:
    try:
        send_request()
        break
    except:
        pass  # Immediate retry, hammers server
```

## Platform-Specific Guidance

### Web/API
- **Primary risks:** Unclosed DB connections, no request timeouts, no circuit breakers, retry storms
- **Key review areas:** HTTP client calls, database queries, middleware error handling
- **Best practices:** Connection pools, request timeouts, circuit breakers (Hystrix, resilience4j)

### Android
- **Primary risks:** Process death without state restoration, uncaught exceptions in background threads, resource leaks
- **Key review areas:** Activity/Fragment lifecycle, background tasks, database cursors, Bitmap recycling
- **Best practices:** SavedStateHandle, WorkManager for durable tasks, ViewModel for transient state

### iOS
- **Primary risks:** Background task expiry, retain cycles, file handles not closed, Core Data threading violations
- **Key review areas:** BGTaskScheduler, [weak self] in closures, FileHandle, NSManagedObjectContext threading
- **Best practices:** BGTask expiration handlers, weak references, defer for cleanup

### Microservices
- **Primary risks:** Cascading failures, no circuit breakers, missing health checks, retry storms across services
- **Key review areas:** Service-to-service calls, message queue handlers, distributed locks
- **Best practices:** Circuit breakers, bulkheads, health/liveness probes, DLQ for failed messages

## Review Instructions

### Step 1: Audit Error Handling
```bash
# Find bare except/catch
rg "except:\s*$|catch\s*\(.*\)\s*\{\s*\}|catch\s*\{" --type py --type js

# Find swallowed exceptions
rg "except.*:\s*(pass|continue|return None)" --type py
rg "catch.*\{\s*\}" --type js
```

**Safe error handling:**
```python
# ✅ GOOD
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    # Propagate or handle gracefully
    return fallback_value()
except Exception as e:
    logger.exception("Unexpected error")
    raise  # Don't swallow
```

### Step 2: Check Resource Cleanup
```bash
# Find file operations without context manager
rg "open\(.*\)[^with]" --type py
rg "FileHandle.*forReadingAtPath" --type swift
```

**Safe resource handling:**
```python
# ✅ GOOD: Context manager
with open('file.txt') as f:
    data = f.read()
# File closed automatically even if exception

# ✅ GOOD: Go defer
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()  // Always called
    // process file
}
```

### Step 3: Validate Timeouts
```bash
# Find network calls without timeout
rg "requests\.(get|post)\([^)]*\)(?!.*timeout)" --type py
rg "fetch\([^)]*\)(?!.*signal)" --type js
rg "URLSession.*dataTask" --type swift
```

**Safe timeout handling:**
```python
# ✅ GOOD
response = requests.get(url, timeout=10)

# ✅ GOOD: Context with timeout (Go)
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
resp, err := client.Do(req.WithContext(ctx))
```

### Step 4: Implement Graceful Degradation
```python
# ❌ UNSAFE
recommendations = fetch_recommendations()  # Blocks, fails page
render_page(recommendations)

# ✅ GOOD: Graceful fallback
try:
    recommendations = fetch_recommendations(timeout=2)
except TimeoutError:
    recommendations = get_cached_recommendations()
except Exception as e:
    logger.warning(f"Recommendations unavailable: {e}")
    recommendations = []  # Empty, page still loads
render_page(recommendations)
```

### Step 5: Add Exponential Backoff
```python
# ❌ UNSAFE
for _ in range(10):
    try:
        return send_request()
    except:
        pass  # Immediate retry

# ✅ GOOD: Exponential backoff with jitter
import time
import random

max_retries = 5
for attempt in range(max_retries):
    try:
        return send_request()
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        wait = (2 ** attempt) + random.uniform(0, 1)
        logger.warning(f"Retry {attempt+1}/{max_retries} after {wait}s")
        time.sleep(wait)
```

## Platform-Specific Examples

### Android: Process Death Handling
```kotlin
// ❌ UNSAFE: State lost on process death
class MyActivity : AppCompatActivity() {
    private var userId: String? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        userId = intent.getStringExtra("USER_ID")  // Lost on process death
    }
}

// ✅ SAFE: SavedStateHandle
class MyViewModel(private val savedState: SavedStateHandle) : ViewModel() {
    private val userId: String? = savedState.get("USER_ID")
    
    fun setUserId(id: String) {
        savedState["USER_ID"] = id  // Survives process death
    }
}
```

### iOS: Background Task Expiry
```swift
// ❌ UNSAFE: No expiration handler
func scheduleBackgroundTask() {
    BGTaskScheduler.shared.register(forTaskWithIdentifier: "sync", using: nil) { task in
        performLongSync()
        task.setTaskCompleted(success: true)
    }
}

// ✅ SAFE: Expiration handler
func scheduleBackgroundTask() {
    BGTaskScheduler.shared.register(forTaskWithIdentifier: "sync", using: nil) { task in
        var isCancelled = false
        task.expirationHandler = {
            isCancelled = true
            cleanupPartialSync()
        }
        performLongSync(checkCancellation: { isCancelled })
        task.setTaskCompleted(success: !isCancelled)
    }
}
```

### Microservices: Circuit Breaker
```python
# ❌ UNSAFE: No circuit breaker
def call_recommendation_service():
    return requests.get('http://recommendations/api', timeout=5)

# ✅ SAFE: Circuit breaker
from pybreaker import CircuitBreaker

recommendation_breaker = CircuitBreaker(fail_max=5, timeout_duration=60)

@recommendation_breaker
def call_recommendation_service():
    return requests.get('http://recommendations/api', timeout=5)

# Caller handles CircuitBreakerError
try:
    recommendations = call_recommendation_service()
except CircuitBreakerError:
    recommendations = get_cached_recommendations()
```

## Migration Coverage

## Quick Checklist
- [ ] All exceptions caught with specific types (not bare except)
- [ ] Resources cleaned up in all code paths (with/defer/finally)
- [ ] Network calls have timeouts
- [ ] Locks acquired with timeout, not infinite wait
- [ ] Non-critical dependencies have fallback values
- [ ] Retries use exponential backoff with jitter
- [ ] Max retry attempts enforced
- [ ] Errors logged before propagation/handling
- [ ] Mobile state survives process death (SavedStateHandle/NSCoding)
- [ ] Background tasks handle expiration gracefully
