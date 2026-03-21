# Task: Off-by-One Error

## Category
correctness

## Severity
medium

## Platforms
all

## Languages
all

## Description
Boundary errors in loops, array indexing, or range calculations where the count is one too many or one too few, causing missed elements, out-of-bounds access, or incorrect results.

## Detection Heuristics
- Loop bounds using `<=` with length (should be `<`)
- Array access at `array[length]` (out of bounds)
- Fence-post errors in pagination (skip/offset calculations)
- Substring/slice with wrong end index
- Range calculations forgetting inclusive vs exclusive boundaries

## Eval Cases

### Case 1: Loop bound error
```c
int arr[10];
for (int i = 0; i <= 10; i++) {
    arr[i] = 0;  // arr[10] is out of bounds
}
```
**Expected finding:** Medium — Off-by-one. Loop iterates to `i=10` but array has indices 0-9. Use `i < 10`.

### Case 2: Pagination skip error
```javascript
function getPage(items, page, pageSize) {
  const start = page * pageSize; // page 1 skips first pageSize items
  return items.slice(start, start + pageSize);
}
```
**Expected finding:** Medium — Off-by-one in pagination. If `page` is 1-indexed, first page skips items. Use `(page - 1) * pageSize`.

## Counter-Examples

### Counter 1: Correct loop bound
```c
int arr[10];
for (int i = 0; i < 10; i++) {
    arr[i] = 0;
}
```
**Why it's correct:** Loop bound is exclusive, matching array size.

## Binary Eval Assertions
- [ ] Detects OOB access in eval case 1
- [ ] Detects pagination skip error in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the off-by-one boundary
- [ ] Severity assigned as medium
