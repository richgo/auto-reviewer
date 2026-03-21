---
name: performance
description: >
  Detect performance issues: N+1 query problems, algorithmic complexity issues, memory leaks,
  unbounded growth. Trigger when reviewing database queries, loops, collections, memory allocation,
  or any code that processes large datasets or high-frequency operations.
---

# Performance Review

## Purpose
Review code for performance issues that cause slow response times, high resource usage, or scalability problems.

## Scope
Four universal performance issue classes plus platform-specific patterns:
1. **N+1 Queries** — sequential database queries in loops
2. **Algorithmic Complexity** — O(n²) or worse where O(n log n) possible
3. **Memory Leaks** — unreleased resources, references preventing GC
4. **Unbounded Growth** — collections/caches without size limits

**Platform-specific:**
- **Android:** Overdraw, bitmap memory, startup time
- **iOS:** Main thread work, autolayout performance, large asset loading
- **Web:** Bundle size, unnecessary re-renders, Core Web Vitals
- **Microservices:** Latency chains, connection pool exhaustion, payload bloat

## Detection Strategy

### Universal Red Flags
- **Queries in loops** — `for item in items: db.query(...)`
- **Nested loops** — O(n²) complexity
- **Large in-memory collections** — loading all records without pagination
- **Missing cache invalidation** — unbounded cache growth
- **Resource leaks** — files/connections not closed

### High-Risk Patterns

**N+1 Queries:**
```python
# ❌ N+1: One query + N queries in loop
users = User.objects.all()
for user in users:
    posts = Post.objects.filter(user=user)  # N queries

# ✅ Eager loading
users = User.objects.prefetch_related('posts')
```

**Algorithmic Complexity:**
```python
# ❌ O(n²) nested loop
for i in items:
    for j in items:
        if i == j:
            ...

# ✅ O(n) with set
items_set = set(items)
for i in items:
    if i in items_set:
        ...
```

**Memory Leak:**
```python
# ❌ Global cache without size limit
cache = {}
def get_data(key):
    if key not in cache:
        cache[key] = expensive_operation(key)
    return cache[key]

# ✅ LRU cache with max size
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_data(key):
    return expensive_operation(key)
```

## Platform-Specific Guidance

### Web
- **Bundle size:** Analyze imports, use code splitting
- **Re-renders:** Check React/Vue memoization
- **Core Web Vitals:** Optimize LCP, CLS, INP

### Android
- **Main thread:** Move I/O to background threads
- **Bitmap memory:** Downsample images, use image libraries
- **Overdraw:** Reduce nested backgrounds

### iOS
- **Main queue:** Move heavy work to background
- **Autolayout:** Simplify constraint hierarchies
- **Asset loading:** Downsample large images

### Microservices
- **Serial calls:** Parallelize independent service calls
- **Connection pools:** Configure appropriate sizes
- **Over-fetching:** Use field selection/projections

## Review Instructions

### Step 1: Identify Hotspots
- Database query patterns
- Loops and nested loops
- Collection operations
- Memory allocations
- I/O operations

### Step 2: Analyze Complexity
- Calculate Big-O complexity
- Identify unnecessary iterations
- Check for redundant operations

### Step 3: Check Resource Management
- Files/connections closed properly
- Caches have size limits
- Pagination for large datasets
- Proper use of generators/streams

### Step 4: Platform-Specific Checks
See platform-specific guidance above

### Step 5: Report Findings
- **Severity:** High (N+1, O(n²) in critical path), Medium (unbounded growth, leaks)
- **Location:** File, line, function
- **Description:** Performance impact
- **Fix:** Optimized code example

## Related Review Tasks
- `review-tasks/performance/n-plus-one.md`
- `review-tasks/performance/algorithmic-complexity.md`
- `review-tasks/performance/memory-leak.md`
- `review-tasks/performance/unbounded-growth.md`
- Platform-specific tasks in `android/`, `ios/`, `web/`, `microservices/`

## Quick Checklist
- [ ] No N+1 queries (use eager loading)
- [ ] Algorithmic complexity reasonable (< O(n²))
- [ ] Caches have size limits
- [ ] Pagination for large datasets
- [ ] Resources properly closed
- [ ] No blocking I/O on UI/main thread
- [ ] Collections use appropriate data structures
