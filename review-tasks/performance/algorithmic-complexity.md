# Task: Algorithmic Complexity

## Category
performance

## Severity
medium

## Platforms
all

## Languages
all

## Description
Unnecessarily expensive algorithms — O(n²) or worse when O(n) or O(n log n) solutions exist. Includes nested loops over collections, repeated linear searches, and quadratic string building.

## Detection Heuristics
- Nested loops over same or related collections
- `Array.includes()` or `list.index()` inside a loop (O(n²))
- String concatenation in a loop (quadratic in some languages)
- Sorting inside a loop
- Repeated full-collection scans instead of building a lookup map

## Eval Cases

### Case 1: Nested loop for matching
```python
def find_common(list_a, list_b):
    common = []
    for a in list_a:
        for b in list_b:
            if a == b:
                common.append(a)
    return common
```
**Expected finding:** Medium — O(n×m) nested loop. Convert one list to a set for O(n+m): `set_b = set(list_b); return [a for a in list_a if a in set_b]`

### Case 2: Includes in loop
```javascript
function removeDuplicates(items) {
  const unique = [];
  for (const item of items) {
    if (!unique.includes(item)) { // O(n) check per iteration
      unique.push(item);
    }
  }
  return unique;
}
```
**Expected finding:** Medium — O(n²) due to `includes()` in loop. Use `Set`: `return [...new Set(items)]`

## Counter-Examples

### Counter 1: Set-based lookup
```python
def find_common(list_a, list_b):
    set_b = set(list_b)
    return [a for a in list_a if a in set_b]
```
**Why it's correct:** Set lookup is O(1), total is O(n+m).

## Binary Eval Assertions
- [ ] Detects O(n²) in eval case 1
- [ ] Detects O(n²) in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the complexity and suggests improvement
- [ ] Severity assigned as medium
