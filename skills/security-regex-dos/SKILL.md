---
name: security regex dos
description: >
  Migrated review-task skill for Regular Expression Denial of Service (ReDoS). Use this
  skill whenever diffs may introduce security issues on all, especially in all. Actively
  look for: ReDoS occurs when regular expressions with catastrophic backtracking are
  applied to user-controlled input, causing exponential time complexity and... and
  report findings with medium severity expectations and actionable fixes.
---

# Regular Expression Denial of Service (ReDoS)

## Source Lineage
- Original review task: `review-tasks/security/regex-dos.md`
- Migrated skill artifact: `skills/review-task-security-regex-dos/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
ReDoS occurs when regular expressions with catastrophic backtracking are applied to user-controlled input, causing exponential time complexity and CPU exhaustion with carefully crafted inputs.

## Detection Heuristics
- Nested quantifiers: `(a+)+`, `(a*)*`, `(a+)*`, `(a|a)*`
- Alternation with overlapping patterns: `(a|ab)+`
- Regex on unbounded user input without timeout
- Missing input length validation before regex matching
- Complex patterns with backtracking on email/URL validation

## Eval Cases
### Case 1: Nested quantifiers
```python
# BUGGY CODE — should be detected
import re
def validate_input(user_input):
    pattern = r'^(a+)+$'
    return re.match(pattern, user_input) is not None
```
**Expected finding:** Medium — ReDoS vulnerability via nested quantifiers `(a+)+`. Input `aaaaaaaaaaaaaaaaaaaaX` causes exponential backtracking (2^n). Use atomic groups or possessive quantifiers, or validate input length first.

### Case 2: Overlapping alternation
```javascript
// BUGGY CODE — should be detected
function validateEmail(email) {
  const regex = /^([a-zA-Z0-9]+|[a-zA-Z0-9]+\.[a-zA-Z0-9]+)*@example\.com$/;
  return regex.test(email);
}
```
**Expected finding:** Medium — ReDoS via overlapping alternation `(a+|a+\.a+)*`. String with many dots causes catastrophic backtracking. Use simpler non-overlapping patterns or third-party email validator libraries.

### Case 3: Unbounded regex on user input
```java
// BUGGY CODE — should be detected
public boolean matches(String userInput) {
    String pattern = "^(a|ab)*c$";
    return userInput.matches(pattern);
}
```
**Expected finding:** Medium — ReDoS with overlapping alternation `(a|ab)*`. No input length check. Input `aaaaaaaaaaaaaaaaaaa` (no 'c') causes exponential backtracking. Limit input length or use regex timeout (Java 9+: `Pattern.compile(pattern).matcher(input).matches()` with interruptible thread).

## Counter-Examples
### Counter 1: Input length validation before regex
```python
# CORRECT CODE — should NOT be flagged
import re
def validate_input(user_input):
    if len(user_input) > 100:
        return False
    pattern = r'^[a-zA-Z0-9]{1,50}$'  # No nested quantifiers
    return re.match(pattern, user_input) is not None
```
**Why it's correct:** Input length limited, simple character class without backtracking risk.

### Counter 2: Library for complex validation
```javascript
// CORRECT CODE — should NOT be flagged
const validator = require('validator');
function validateEmail(email) {
  return validator.isEmail(email);
}
```
**Why it's correct:** Using battle-tested library instead of custom regex for email validation.

## Binary Eval Assertions
- [ ] Detects nested quantifiers in eval case 1
- [ ] Detects overlapping alternation in eval case 2
- [ ] Detects unbounded regex in eval case 3
- [ ] Does NOT flag counter-example 1 (length check + simple pattern)
- [ ] Does NOT flag counter-example 2 (validator library)
- [ ] Finding explains backtracking behavior
- [ ] Severity assigned as medium (high if no rate limiting)

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
