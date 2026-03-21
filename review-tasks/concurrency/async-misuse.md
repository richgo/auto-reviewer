# Task: Async/Await Misuse

## Category
concurrency

## Severity
high

## Platforms
all

## Languages
javascript, typescript, python, csharp, rust

## Description
Missing awaits, fire-and-forget promises, unhandled rejections, or blocking the event loop — leading to silent failures, data loss, or degraded performance.

## Detection Heuristics
- Async function called without `await` (fire-and-forget)
- `.then()` chain without `.catch()`
- `async` function return value ignored
- Blocking sync calls inside async context (sync I/O in Node.js event loop)
- Python `asyncio.create_task()` without storing reference (task may be GC'd)

## Eval Cases

### Case 1: Missing await
```javascript
async function saveAndNotify(data) {
  await db.save(data);
  emailService.sendNotification(data.userId); // returns Promise, not awaited
  return { success: true };
}
```
**Expected finding:** High — Missing await on `emailService.sendNotification()`. Errors will be unhandled rejections; function returns before notification completes.

### Case 2: Python fire-and-forget task
```python
async def handle_request(data):
    asyncio.create_task(process_background(data))  # no reference stored
    return {"status": "accepted"}
```
**Expected finding:** Medium — Task created without storing reference. If no strong reference exists, the task may be garbage collected before completion. Store in a set: `background_tasks.add(task)`

## Counter-Examples

### Counter 1: Properly awaited
```javascript
async function saveAndNotify(data) {
  await db.save(data);
  await emailService.sendNotification(data.userId);
  return { success: true };
}
```
**Why it's correct:** Both async operations are awaited.

## Binary Eval Assertions
- [ ] Detects missing await in eval case 1
- [ ] Detects fire-and-forget task in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies which async call is not awaited
- [ ] Finding explains the consequence (unhandled errors, data loss)
