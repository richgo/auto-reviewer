# Task: Memory Leak

## Category
performance

## Severity
high

## Platforms
all

## Languages
all

## Description
Unbounded accumulation of objects in memory — event listeners not removed, caches without eviction, closures capturing large scopes, subscriptions not unsubscribed.

## Detection Heuristics
- Event listeners added without corresponding removal
- Objects appended to collections that are never pruned
- React `useEffect` with subscriptions but no cleanup return
- Closures capturing large objects unnecessarily
- Global caches without TTL or size limits

## Eval Cases

### Case 1: React effect without cleanup
```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    const socket = new WebSocket(`/ws/${roomId}`);
    socket.onmessage = (e) => setMessages(m => [...m, e.data]);
    // no cleanup — socket never closed on unmount/re-render
  }, [roomId]);
  return <div>...</div>;
}
```
**Expected finding:** High — Memory leak. WebSocket opened in useEffect without cleanup function. Add `return () => socket.close();`

### Case 2: Unbounded cache
```python
_cache = {}

def get_user_profile(user_id):
    if user_id not in _cache:
        _cache[user_id] = db.fetch_user(user_id)
    return _cache[user_id]
```
**Expected finding:** Medium — Unbounded cache. `_cache` grows indefinitely. Use `functools.lru_cache` or add TTL/max-size eviction.

## Counter-Examples

### Counter 1: Effect with cleanup
```jsx
useEffect(() => {
  const socket = new WebSocket(`/ws/${roomId}`);
  socket.onmessage = (e) => setMessages(m => [...m, e.data]);
  return () => socket.close();
}, [roomId]);
```
**Why it's correct:** Cleanup function closes socket on unmount.

## Binary Eval Assertions
- [ ] Detects missing cleanup in eval case 1
- [ ] Detects unbounded cache in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the leak source
- [ ] Finding suggests cleanup mechanism
