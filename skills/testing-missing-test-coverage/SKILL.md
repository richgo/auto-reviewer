---
name: testing missing test coverage
description: >
  Missing Test Coverage. Use this skill whenever diffs
  may introduce testing issues on all, especially in all. Actively look for: New code
  paths, branches, or error cases introduced without corresponding tests. Includes new
  functions without tests, new conditional... and report findings with medium severity
  expectations and actionable fixes.
---

# Missing Test Coverage
## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
New code paths, branches, or error cases introduced without corresponding tests. Includes new functions without tests, new conditional branches not covered, and modified logic without updated tests.

## Detection Heuristics
- New public functions/methods with no corresponding test file changes
- New `if/else` branches without tests exercising both paths
- Error handling paths (catch blocks) without error-case tests
- New API endpoints without integration tests
- Modified business logic without updated assertions

## Eval Cases
### Case 1: New function, no tests
```python
# In PR diff: new file payment_processor.py
class PaymentProcessor:
    def process(self, amount, currency):
        if currency not in SUPPORTED_CURRENCIES:
            raise UnsupportedCurrencyError(currency)
        if amount <= 0:
            raise InvalidAmountError(amount)
        return self.gateway.charge(amount, currency)
```
**Expected finding:** Medium — New `PaymentProcessor.process()` with 3 code paths (success, unsupported currency, invalid amount) but no test file in the diff. Add tests covering all branches.

### Case 2: New branch, no test update
```javascript
// BEFORE (existing, tested):
function getDiscount(user) {
  return user.isPremium ? 0.2 : 0;
}

// AFTER (in PR diff):
function getDiscount(user) {
  if (user.isEmployee) return 0.5;  // new branch
  return user.isPremium ? 0.2 : 0;
}
// No changes to getDiscount.test.js
```
**Expected finding:** Medium — New `isEmployee` branch added but test file not updated. Add test for employee discount case.

## Counter-Examples
### Counter 1: Tests included in same PR
```
# PR includes both:
# - src/payment_processor.py (new code)
# - tests/test_payment_processor.py (tests for all branches)
```
**Why it's correct:** Tests are co-located with the new code in the same PR.

## Binary Eval Assertions
- [ ] Detects untested new function in eval case 1
- [ ] Detects untested new branch in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies specific untested paths
- [ ] Severity assigned as medium
