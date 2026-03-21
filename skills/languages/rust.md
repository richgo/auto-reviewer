---
name: rust
description: >
  Rust-specific code review: unsafe blocks, lifetime issues, Send/Sync violations, error handling,
  async pitfalls. Trigger when reviewing Rust (.rs) files, especially unsafe code, FFI, async/await,
  or concurrent programming patterns.
---

# Language-Specific Review: Rust

## Purpose
Rust-specific guidance: unsafe code, lifetimes, concurrency, error handling, and async patterns.

## Key Areas

### 1. Unsafe Code
```rust
// ❌ UNSAFE: Undefined behavior
unsafe {
    let ptr = std::ptr::null_mut::<i32>();
    *ptr = 42;  // Dereferencing null pointer
}

// ✅ SAFE: Validate before unsafe
unsafe {
    if !ptr.is_null() {
        *ptr = 42;
    }
}

// Document safety invariants
/// SAFETY: ptr must be valid and aligned
unsafe fn write_value(ptr: *mut i32, value: i32) {
    *ptr = value;
}
```

### 2. Lifetime Issues
```rust
// ❌ UNSAFE: Dangling reference
fn get_str() -> &str {
    let s = String::from("hello");
    &s  // Returns reference to dropped value
}

// ✅ SAFE: Return owned value
fn get_str() -> String {
    String::from("hello")
}

// ❌ UNSAFE: Lifetime mismatch
struct Parser<'a> {
    data: &'a str,
}

impl Parser<'_> {
    fn parse(&self) -> &str {
        &self.data[..]  // OK, but callers might misuse
    }
}

// ✅ GOOD: Explicit lifetime
impl<'a> Parser<'a> {
    fn parse(&self) -> &'a str {
        &self.data[..]
    }
}
```

### 3. Send/Sync Violations
```rust
// ❌ UNSAFE: Rc across threads
use std::rc::Rc;

let data = Rc::new(42);
std::thread::spawn(move || {
    println!("{}", data);  // Rc is not Send!
});

// ✅ SAFE: Arc for thread-safe reference counting
use std::sync::Arc;

let data = Arc::new(42);
std::thread::spawn(move || {
    println!("{}", data);
});
```

### 4. Error Handling
```rust
// ❌ BAD: unwrap in library code
fn parse_config(path: &str) -> Config {
    let content = std::fs::read_to_string(path).unwrap();
    serde_json::from_str(&content).unwrap()
}

// ✅ GOOD: Propagate errors
fn parse_config(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}
```

### 5. Async Pitfalls
```rust
// ❌ BAD: Blocking in async
async fn process() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks executor!
}

// ✅ GOOD: Async sleep
async fn process() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// ❌ BAD: Missing Send bound
async fn process(data: Rc<Data>) {
    // Rc is not Send, function can't be spawned
}

// ✅ GOOD: Use Arc
async fn process(data: Arc<Data>) {
    // Arc is Send + Sync
}
```

## OWASP References
- [C-Based Toolchain Hardening](https://cheatsheetseries.owasp.org/cheatsheets/C-Based_Toolchain_Hardening_Cheat_Sheet.html)

## Quick Checklist
- [ ] Unsafe blocks documented with safety invariants
- [ ] No null pointer dereferences
- [ ] Lifetimes explicit where needed
- [ ] Arc (not Rc) for thread-shared data
- [ ] No .unwrap() in library code
- [ ] Async functions don't block executor
