---
name: observability logging gaps
description: >
  Migrated review-task skill for Logging & Observability Gaps. Use this skill whenever
  diffs may introduce observability issues on all, especially in all. Actively look for:
  Missing or inadequate logging in critical code paths — error handling without logs,
  business operations without audit trail,... and report findings with medium severity
  expectations and actionable fixes.
---

# Logging & Observability Gaps

## Source Lineage
- Original review task: `review-tasks/observability/logging-gaps.md`
- Migrated skill artifact: `skills/review-task-observability-logging-gaps/SKILL.md`

## Task Metadata
- Category: `observability`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Missing or inadequate logging in critical code paths — error handling without logs, business operations without audit trail, or unstructured logs that can't be searched/alerted on.

## Detection Heuristics
- Catch blocks without logging
- Payment/auth/admin operations without audit logging
- `print()` or `console.log()` instead of structured logger
- Missing request ID / correlation ID in distributed systems
- No metrics/counters on critical paths (rate of errors, latency)

## Eval Cases
### Case 1: Silent error handling
```python
try:
    result = payment_gateway.charge(amount)
except PaymentError:
    return {"status": "failed"}  # no log — impossible to debug
```
**Expected finding:** Medium — No logging in error handler. Payment failures will be invisible to operations. Add `logger.error("Payment failed", exc_info=True, extra={"amount": amount})`

### Case 2: Print instead of logger
```python
def process_order(order):
    print(f"Processing order {order.id}")  # not structured, no level, lost in prod
    # ...
    print(f"Order {order.id} completed")
```
**Expected finding:** Low — Using `print()` instead of structured logger. Logs won't be searchable or have severity levels in production. Use `logger.info()`.

## Counter-Examples
### Counter 1: Structured logging
```python
try:
    result = payment_gateway.charge(amount)
except PaymentError as e:
    logger.error("Payment charge failed", extra={
        "amount": amount, "error": str(e), "gateway": "stripe"
    })
    return {"status": "failed"}
```
**Why it's correct:** Error logged with structured context for debugging and alerting.

## Binary Eval Assertions
- [ ] Detects silent error handling in eval case 1
- [ ] Detects print-logging in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests structured logging with context

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
