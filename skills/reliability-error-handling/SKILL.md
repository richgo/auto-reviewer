---
name: reliability error handling
description: >
  Swallowed Errors / Missing Error Handling. Use this
  skill whenever diffs may introduce reliability issues on all, especially in all.
  Actively look for: Catching exceptions without logging, re-throwing, or handling them
  — causing silent failures. Also includes missing try/catch around operations... and
  report findings with high severity expectations and actionable fixes.
---

# Swallowed Errors / Missing Error Handling
## Task Metadata
- Category: `reliability`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Catching exceptions without logging, re-throwing, or handling them — causing silent failures. Also includes missing try/catch around operations that can fail.

## Detection Heuristics
- Empty catch blocks or catch blocks with only `pass`/`return`
- `.catch(() => {})` on promises
- No error handling around I/O, network, or parsing operations
- Generic catch-all that hides specific errors
- Missing error response to caller after failure

## Eval Cases
### Case 1: Empty catch block
```java
try {
    processPayment(order);
} catch (PaymentException e) {
    // silently swallowed
}
order.setStatus("COMPLETED"); // runs even if payment failed
```
**Expected finding:** High — Swallowed exception. Payment failure is silently ignored, order marked as completed. Log the error and handle the failure state.

### Case 2: Promise catch suppression
```javascript
async function syncData() {
  await fetch('/api/sync').catch(() => {}); // errors silently ignored
  console.log('Sync complete'); // logs success even on failure
}
```
**Expected finding:** High — Error suppressed. Failed sync appears successful. Handle or propagate the error.

## Counter-Examples
### Counter 1: Error logged and handled
```java
try {
    processPayment(order);
} catch (PaymentException e) {
    logger.error("Payment failed for order {}", order.getId(), e);
    order.setStatus("PAYMENT_FAILED");
    throw new OrderProcessingException("Payment failed", e);
}
```
**Why it's correct:** Error is logged, state is updated, and exception is propagated.

## Binary Eval Assertions
- [ ] Detects swallowed exception in eval case 1
- [ ] Detects catch suppression in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies the consequence of swallowed error
- [ ] Severity assigned as high
