# Task: Race Condition

## Category
concurrency

## Severity
high

## Platforms
all

## Languages
all

## Description
Multiple threads/coroutines/requests accessing shared mutable state without synchronization, leading to data corruption, lost updates, or inconsistent reads.

## Detection Heuristics
- Read-modify-write on shared state without locking
- Check-then-act patterns without atomic operations
- Global/class-level mutable variables accessed from concurrent handlers
- Database read-then-update without row locking or optimistic concurrency
- Non-thread-safe collections used across threads

## Eval Cases

### Case 1: TOCTOU in balance check
```python
def withdraw(account_id, amount):
    account = Account.query.get(account_id)
    if account.balance >= amount:
        account.balance -= amount
        db.session.commit()
    return account.balance
```
**Expected finding:** High — Race condition (TOCTOU). Two concurrent withdrawals can both pass the balance check before either commits. Use `SELECT ... FOR UPDATE` or optimistic locking.

### Case 2: Shared counter without lock
```java
public class RequestCounter {
    private int count = 0;
    
    public void increment() {
        count++;  // Not atomic
    }
    
    public int getCount() {
        return count;
    }
}
```
**Expected finding:** High — Race condition on shared counter. `count++` is not atomic (read-modify-write). Use `AtomicInteger` or `synchronized`.

### Case 3: Go map concurrent access
```go
var cache = make(map[string]string)

func handleRequest(w http.ResponseWriter, r *http.Request) {
    key := r.URL.Query().Get("key")
    if val, ok := cache[key]; ok {
        fmt.Fprint(w, val)
        return
    }
    val := expensiveCompute(key)
    cache[key] = val  // concurrent map write = panic
    fmt.Fprint(w, val)
}
```
**Expected finding:** High — Concurrent map write in Go causes panic. Use `sync.Map` or protect with `sync.RWMutex`.

## Counter-Examples

### Counter 1: Database row locking
```python
def withdraw(account_id, amount):
    account = Account.query.with_for_update().get(account_id)
    if account.balance >= amount:
        account.balance -= amount
        db.session.commit()
    return account.balance
```
**Why it's correct:** `FOR UPDATE` lock prevents concurrent modifications.

### Counter 2: Atomic integer
```java
public class RequestCounter {
    private final AtomicInteger count = new AtomicInteger(0);
    
    public void increment() {
        count.incrementAndGet();
    }
}
```
**Why it's correct:** AtomicInteger provides thread-safe increment.

## Binary Eval Assertions
- [ ] Detects TOCTOU in eval case 1
- [ ] Detects non-atomic increment in eval case 2
- [ ] Detects concurrent map write in eval case 3
- [ ] Does NOT flag counter-example 1
- [ ] Does NOT flag counter-example 2
- [ ] Finding identifies the shared state and suggests synchronization
- [ ] Severity assigned as high
