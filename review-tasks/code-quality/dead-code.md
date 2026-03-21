# Task: Dead Code / Unused Imports

## Category
code-quality

## Severity
low

## Platforms
all

## Languages
all

## Description
Unreachable code, unused variables, unused imports, or commented-out code blocks left in the codebase. Increases cognitive load and maintenance burden.

## Detection Heuristics
- Imported modules/functions not referenced in the file
- Variables assigned but never read
- Functions defined but never called (within PR scope)
- Code after unconditional return/throw/break
- Large commented-out code blocks (>5 lines)

## Eval Cases

### Case 1: Unused imports
```python
import os
import sys
import json
from datetime import datetime, timedelta

def get_timestamp():
    return datetime.now().isoformat()
# os, sys, json, timedelta are unused
```
**Expected finding:** Low — Unused imports: `os`, `sys`, `json`, `timedelta`. Remove to reduce cognitive load.

### Case 2: Unreachable code
```javascript
function getStatus(code) {
  if (code === 200) return 'ok';
  if (code === 404) return 'not found';
  return 'error';
  console.log('Processing complete'); // unreachable
  updateMetrics(code); // unreachable
}
```
**Expected finding:** Low — Unreachable code after `return` statement. Remove dead code.

## Counter-Examples

### Counter 1: All imports used
```python
import json
from datetime import datetime

def serialize(data):
    return json.dumps({"timestamp": datetime.now().isoformat(), "data": data})
```
**Why it's correct:** Both imports are used in the function.

## Binary Eval Assertions
- [ ] Detects unused imports in eval case 1
- [ ] Detects unreachable code in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding lists specific unused items
- [ ] Severity assigned as low
