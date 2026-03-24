---
name: correctness null deref
description: >
  Null/Undefined Dereference. Use this skill whenever
  diffs may introduce correctness issues on all, especially in all. Actively look for:
  Accessing properties or methods on a value that may be null/undefined/None, causing
  runtime crashes (NullPointerException, TypeError, segfault). and report findings with
  high severity expectations and actionable fixes.
---

# Null/Undefined Dereference
## Task Metadata
- Category: `correctness`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Accessing properties or methods on a value that may be null/undefined/None, causing runtime crashes (NullPointerException, TypeError, segfault).

## Detection Heuristics
- Optional/nullable return values used without null checks
- Array/map lookups used directly without existence verification
- Function parameters not validated before property access
- Chained property access on potentially null intermediate values
- `find()`, `get()`, dictionary access that may return null/undefined

## Eval Cases
### Case 1: Unchecked find result
```javascript
function getUserEmail(users, id) {
  const user = users.find(u => u.id === id);
  return user.email; // user might be undefined
}
```
**Expected finding:** High — Potential null dereference. `Array.find()` returns `undefined` if no match. Add null check or use optional chaining: `user?.email`

### Case 2: Java Map.get without null check
```java
Map<String, Config> configs = loadConfigs();
String value = configs.get(key).getValue(); // get() may return null
```
**Expected finding:** High — Null dereference. `Map.get()` returns null for missing keys. Check for null before calling `.getValue()`.

## Counter-Examples
### Counter 1: Optional chaining
```javascript
function getUserEmail(users, id) {
  const user = users.find(u => u.id === id);
  return user?.email ?? 'unknown';
}
```
**Why it's correct:** Optional chaining handles undefined safely.

## Binary Eval Assertions
- [ ] Detects null deref in eval case 1
- [ ] Detects null deref in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the nullable source
- [ ] Finding suggests null check or optional chaining
