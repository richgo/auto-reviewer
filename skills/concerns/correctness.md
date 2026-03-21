---
name: correctness
description: >
  Detect correctness bugs: null pointer dereferences, off-by-one errors, integer overflow,
  floating-point comparison issues, logic inversions, and platform-specific lifecycle bugs.
  Trigger when reviewing arithmetic, array indexing, null checks, conditionals, or lifecycle methods.
---

# Correctness Review

## Purpose
Review code for logical correctness bugs that cause crashes, wrong results, or unexpected behavior. These are not security vulnerabilities but cause user-facing failures.

## Scope
Five universal correctness bug classes plus platform-specific patterns:
1. **Null Dereference** — accessing null/nil/None without check
2. **Off-by-One** — loop bounds, array indexing errors
3. **Integer Overflow** — arithmetic exceeding type limits
4. **Floating-Point Comparison** — direct equality checks on floats
5. **Logic Inversion** — `if (!condition)` when should be `if (condition)`

**Platform-specific:**
- **Android:** Lifecycle bugs (view access after destroy), config change crashes
- **iOS:** Force unwrap crashes, retain cycles, lifecycle bugs
- **Web:** JavaScript type coercion (`==` vs `===`)
- **Microservices:** Eventual consistency bugs, non-idempotent handlers

## Detection Strategy

### Universal Red Flags
- **Dereferencing without null check**: `obj.method()` without `if (obj != null)`
- **Loop bounds errors**: `for (i = 0; i <= array.length; i++)`
- **Unchecked arithmetic**: `int sum = a + b` (can overflow)
- **Float equality**: `if (f == 0.1)`
- **Inverted boolean**: `if (!isValid)` when should be `if (isValid)`

### High-Risk Patterns

**Null Dereference:**
- `user.name` without `user != null` check
- `?.` (optional chaining) followed by `!` (force unwrap)
- Assuming API always returns non-null

**Off-by-One:**
- `for (i = 0; i <= array.length; i++)`
- `substring(0, length)` when should be `substring(0, length - 1)`
- Fence-post errors in range checks

**Integer Overflow:**
- `int total = a + b;` for large values
- Multiplying timestamps without overflow check
- Array size calculations without bounds check

**Floating-Point Comparison:**
- `if (price == 19.99)`
- `while (x != target)` for floats

**Logic Inversion:**
- `if (!file.exists()) { file.open() }` (inverted)
- Negation mistakes in complex conditions

## Platform-Specific Guidance

### Android
- **Key bugs:** View access after `onDestroyView`, Fragment detached, permission missing
- **Detection:** Accessing `view` in Fragment after destroy, no null-check on `getActivity()`
- **Safe patterns:** `viewLifecycleOwner`, `viewBinding`, null-checks before UI access

### iOS
- **Key bugs:** Force unwrap `!`, retain cycles `[self]`, UIKit access before `viewDidLoad`
- **Detection:** `!` on optionals, closures without `[weak self]`, UI updates from background
- **Safe patterns:** `guard let`, `if let`, `[weak self]`, optional chaining

### Web (JavaScript)
- **Key bugs:** Type coercion (`==`), truthiness errors, `NaN` comparisons
- **Detection:** `==` instead of `===`, `if (value)` when value could be 0/''/false
- **Safe patterns:** `===`, explicit `!= null` checks, `Number.isNaN()`

### Microservices
- **Key bugs:** Reading stale data, non-idempotent handlers, partial failures
- **Detection:** No version checks, missing idempotency keys, no rollback on failure
- **Safe patterns:** Saga pattern, idempotency tokens, eventual consistency handling

## Review Instructions

### Step 1: Trace Null Flows
For each dereference:
1. **Source:** Where does variable come from?
2. **Can be null?** API, database, optional parameter
3. **Checked?** `if (x != null)`, `?.`, `guard let`, etc.

### Step 2: Check Loop Bounds
- **Start:** Usually 0 (or 1 for 1-indexed)
- **End:** `< length` (not `<= length`)
- **Increment:** Correct step size

### Step 3: Review Arithmetic
- **Overflow risk:** Use wider types (`long`, `BigInteger`) or check bounds
- **Division:** Check for zero denominator
- **Floats:** Use epsilon comparison: `Math.abs(a - b) < 0.0001`

### Step 4: Validate Conditionals
- Read condition aloud: "If file does NOT exist, open it" — sounds wrong?
- Check for double negatives
- Verify boolean logic with truth table for complex conditions

### Step 5: Platform-Specific Checks
- **Android:** Check lifecycle methods, Fragment attachment
- **iOS:** Find force unwraps `!`, check retain cycles
- **Web:** Find `==` (should be `===`), check truthiness assumptions
- **Microservices:** Check idempotency, eventual consistency handling

### Step 6: Report Findings
For each bug:
- **Severity:** High (null deref, lifecycle crash), Medium (off-by-one, overflow)
- **Location:** File, line
- **Description:** Crash/bug scenario
- **Fix:** Code example with null check, bounds fix, etc.

## Examples

### ✅ SAFE: Null Check (Java)
```java
if (user != null) {
    String name = user.getName();
}
```

### ❌ UNSAFE: Null Dereference (Java)
```java
String name = user.getName();  // NPE if user is null
```
**Finding:** High — Null pointer exception. Check `user != null` before access.

### ✅ SAFE: Loop Bounds (Python)
```python
for i in range(len(array)):
    print(array[i])
```

### ❌ UNSAFE: Off-by-One (Python)
```python
for i in range(len(array) + 1):
    print(array[i])  # IndexError on last iteration
```
**Finding:** High — Off-by-one error. Use `range(len(array))` without `+ 1`.

### ✅ SAFE: Float Comparison (Python)
```python
if abs(price - 19.99) < 0.01:
    apply_discount()
```

### ❌ UNSAFE: Direct Float Equality (Python)
```python
if price == 19.99:  # May fail due to floating-point precision
    apply_discount()
```
**Finding:** Medium — Float equality check unreliable. Use epsilon comparison.

### ✅ SAFE: iOS Optional Unwrap (Swift)
```swift
guard let user = user else { return }
let name = user.name
```

### ❌ UNSAFE: Force Unwrap (Swift)
```swift
let name = user!.name  // Crash if user is nil
```
**Finding:** High — Force unwrap crash risk. Use `guard let` or `if let`.

## Related Review Tasks
- `review-tasks/correctness/null-deref.md`
- `review-tasks/correctness/off-by-one.md`
- `review-tasks/correctness/integer-overflow.md`
- `review-tasks/correctness/floating-point-comparison.md`
- `review-tasks/correctness/logic-inversion.md`
- Platform-specific tasks in `android/`, `ios/`, `web/`, `microservices/`

## Quick Checklist
- [ ] All dereferences have null checks
- [ ] Loop bounds use `< length`, not `<= length`
- [ ] Integer arithmetic checked for overflow
- [ ] Float comparisons use epsilon
- [ ] Boolean logic verified (no inversions)
- [ ] Platform lifecycle methods used correctly
- [ ] No force unwraps in production code (iOS)
- [ ] Use `===` instead of `==` (JavaScript)
