# Task: [NAME]

## Category
[security | concurrency | correctness | testing | performance | reliability | api-design | data | observability | code-quality]

## Severity
[critical | high | medium | low]

## Platforms
[all | web | api | mobile | library]

## Languages
[all | list specific languages where this is most relevant]

## Description
What this bug class is and why it matters.

## Detection Heuristics
Patterns and signals to look for in code diffs:
- ...
- ...

## Eval Cases

### Case 1: [brief description]
```language
// BUGGY CODE — should be detected
```
**Expected finding:** [what the reviewer should flag, with severity]

### Case 2: [brief description]
```language
// BUGGY CODE — should be detected
```
**Expected finding:** [what the reviewer should flag]

## Counter-Examples

### Counter 1: [brief description]
```language
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** [explanation of why this is safe despite looking similar]

## Binary Eval Assertions
- [ ] Detects the bug in eval case 1
- [ ] Detects the bug in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes file and line reference
- [ ] Finding includes actionable fix suggestion
- [ ] Severity is correctly assigned
