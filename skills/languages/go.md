---
name: go
description: >
  Go-specific code review: goroutine leaks, error handling patterns, nil interfaces, defer pitfalls,
  context cancellation. Trigger when reviewing Go (.go) files, microservices, or backend services
  using goroutines, channels, and context propagation.
---

# Language-Specific Review: Go

## Purpose
Go-specific guidance: goroutines, error handling, interfaces, context, and Go idioms.

## Key Areas

### 1. Goroutine Leaks
```go
// ❌ UNSAFE: Goroutine leak
func process() {
    go func() {
        for {
            work()  // Never exits
        }
    }()
}

// ✅ SAFE: Context cancellation
func process(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return
            default:
                work()
            }
        }
    }()
}
```

### 2. Error Handling
```go
// ❌ BAD: Ignoring errors
result, _ := doSomething()

// ✅ GOOD: Check errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething failed: %w", err)
}

// ❌ BAD: Panic in library code
func divide(a, b int) int {
    if b == 0 {
        panic("division by zero")
    }
    return a / b
}

// ✅ GOOD: Return error
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

### 3. Nil Interfaces
```go
// ❌ UNSAFE: Nil interface trap
func returnsError() error {
    var err *MyError  // Typed nil
    return err  // Non-nil interface!
}

if err := returnsError(); err != nil {
    // Always true even though err is nil!
}

// ✅ SAFE: Return explicit nil
func returnsError() error {
    var err *MyError
    if err == nil {
        return nil  // Untyped nil
    }
    return err
}
```

### 4. Defer Pitfalls
```go
// ❌ BAD: Defer in loop
for _, file := range files {
    f, _ := os.Open(file)
    defer f.Close()  // All defers execute at function end, not loop iteration
}

// ✅ GOOD: Closure for defers
for _, file := range files {
    func() {
        f, _ := os.Open(file)
        defer f.Close()  // Executes at closure end
        process(f)
    }()
}
```

### 5. Context Cancellation
```go
// ❌ UNSAFE: No timeout
resp, err := http.Get(url)

// ✅ SAFE: Context with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
resp, err := http.DefaultClient.Do(req)
```

## OWASP References
- [Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

## Quick Checklist
- [ ] Goroutines have cancellation mechanism
- [ ] All errors checked (no _ := err)
- [ ] Context passed to blocking operations
- [ ] Defer not in loops
- [ ] Nil interface traps avoided
