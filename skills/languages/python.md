---
name: python
description: >
  Python-specific code review guidance: Django/Flask security, common pitfalls (mutable defaults,
  GIL misunderstanding, exception handling), idioms (context managers, comprehensions), and
  anti-patterns. Trigger when reviewing Python code (.py files) or Django/Flask applications.
---

# Language-Specific Review: Python

## Purpose
Provide Python-specific security, correctness, and style guidance for code review. Covers framework-specific issues (Django, Flask) and Python language pitfalls.

## Scope
- **Framework security:** Django ORM injection, Flask Jinja2 escaping, debug mode
- **Language pitfalls:** Mutable defaults, late binding closures, GIL misunderstanding
- **Common anti-patterns:** Bare `except:`, not using context managers, inefficient loops
- **Security-specific:** Pickle deserialization, `eval()`, path traversal, subprocess

## Framework-Specific Guidance

### Django Security
**Common vulnerabilities:**
1. **Raw SQL with user input:**
   ```python
   # ❌ UNSAFE
   User.objects.raw(f"SELECT * FROM users WHERE name = '{username}'")
   
   # ✅ SAFE
   User.objects.filter(name=username)
   ```

2. **Template auto-escaping bypass:**
   ```python
   # ❌ UNSAFE
   {{ user_bio | safe }}
   
   # ✅ SAFE
   {{ user_bio }}  # Auto-escaped
   ```

3. **Mass assignment:**
   ```python
   # ❌ UNSAFE
   user.update(**request.POST)
   
   # ✅ SAFE
   form = UserForm(request.POST)
   if form.is_valid():
       user.update(**form.cleaned_data)
   ```

4. **Debug mode in production:**
   ```python
   # ❌ UNSAFE
   DEBUG = True  # In production settings
   
   # ✅ SAFE
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ```

**OWASP Django references:**
- [Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)
- [Django REST Framework](https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html)

### Flask Security
**Common vulnerabilities:**
1. **Template injection:**
   ```python
   # ❌ UNSAFE
   template = Template(user_input)
   return template.render()
   
   # ✅ SAFE
   return render_template('page.html', user_input=user_input)
   ```

2. **Secret key hardcoded:**
   ```python
   # ❌ UNSAFE
   app.config['SECRET_KEY'] = 'abc123'
   
   # ✅ SAFE
   app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
   ```

3. **CORS wildcard with credentials:**
   ```python
   # ❌ UNSAFE
   CORS(app, origins='*', supports_credentials=True)
   
   # ✅ SAFE
   CORS(app, origins=['https://example.com'])
   ```

## Common Python Pitfalls

### 1. Mutable Default Arguments
```python
# ❌ UNSAFE
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ SAFE
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
**Finding:** Medium — Mutable default argument. List shared across calls.

### 2. Late Binding Closures
```python
# ❌ UNSAFE
funcs = [lambda: i for i in range(3)]
# All return 2 (last value)

# ✅ SAFE
funcs = [lambda i=i: i for i in range(3)]
```
**Finding:** Low — Late binding closure. Capture variable with default argument.

### 3. Bare Except
```python
# ❌ UNSAFE
try:
    do_something()
except:  # Catches KeyboardInterrupt, SystemExit
    log_error()

# ✅ SAFE
try:
    do_something()
except Exception as e:  # Doesn't catch system exits
    log_error(e)
```
**Finding:** Medium — Bare `except:` catches system exits. Use `except Exception:`.

### 4. Not Using Context Managers
```python
# ❌ UNSAFE
f = open('file.txt')
data = f.read()
f.close()  # Might not be called if exception occurs

# ✅ SAFE
with open('file.txt') as f:
    data = f.read()
```
**Finding:** Low — File not closed on exception. Use `with` statement.

### 5. GIL Misunderstanding
```python
# ❌ INEFFICIENT (for CPU-bound work)
import threading
threads = [threading.Thread(target=cpu_intensive) for _ in range(10)]

# ✅ BETTER
import multiprocessing
processes = [multiprocessing.Process(target=cpu_intensive) for _ in range(10)]
```
**Finding:** Low — Threading for CPU-bound work. Use `multiprocessing` or asyncio for I/O.

## Security-Specific Patterns

### 1. Command Injection
```python
# ❌ UNSAFE
import subprocess
subprocess.call(f"ls {user_path}", shell=True)

# ✅ SAFE
subprocess.call(['ls', user_path], shell=False)
```

### 2. Insecure Deserialization
```python
# ❌ UNSAFE
import pickle
data = pickle.loads(user_input)  # RCE risk

# ✅ SAFE
import json
data = json.loads(user_input)
```

### 3. Path Traversal
```python
# ❌ UNSAFE
filepath = f"/uploads/{filename}"
with open(filepath) as f:
    return f.read()

# ✅ SAFE
import os
from werkzeug.utils import secure_filename
filename = secure_filename(filename)
filepath = os.path.join('/uploads', filename)
if not os.path.realpath(filepath).startswith('/uploads'):
    abort(400)
```

### 4. Eval/Exec with User Input
```python
# ❌ UNSAFE
result = eval(user_expression)

# ✅ SAFE
# Use ast.literal_eval for literals only
import ast
result = ast.literal_eval(user_expression)
```

### 5. SQL Injection
```python
# ❌ UNSAFE
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ SAFE
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Python Idioms to Encourage

### 1. List Comprehensions
```python
# ✅ GOOD
squares = [x**2 for x in range(10)]

# ❌ VERBOSE
squares = []
for x in range(10):
    squares.append(x**2)
```

### 2. Dict/Set Comprehensions
```python
# ✅ GOOD
user_map = {u.id: u.name for u in users}
unique_ids = {u.id for u in users}
```

### 3. Generator Expressions (for large datasets)
```python
# ✅ MEMORY EFFICIENT
total = sum(x**2 for x in huge_list)

# ❌ MEMORY WASTE
total = sum([x**2 for x in huge_list])
```

### 4. F-strings (Python 3.6+)
```python
# ✅ GOOD
message = f"Hello, {name}!"

# ❌ OLD STYLE
message = "Hello, {}!".format(name)
```

### 5. Walrus Operator (Python 3.8+)
```python
# ✅ GOOD
if (match := pattern.search(text)):
    return match.group(1)

# ❌ REDUNDANT
match = pattern.search(text)
if match:
    return match.group(1)
```

## Anti-Patterns to Flag

1. **String concatenation in loops:** Use `''.join()` or f-strings
2. **Checking type with `type(x) == str`:** Use `isinstance(x, str)`
3. **Not using `with` for files/locks:** Resource leaks
4. **Mutable default arguments:** Use `None` and initialize inside
5. **Importing `*`:** Makes namespace unclear
6. **Not using virtual environments:** Dependency conflicts

## Async/Await Patterns

### Correct Usage
```python
# ✅ GOOD: Parallel async
import asyncio
results = await asyncio.gather(fetch(url1), fetch(url2), fetch(url3))

# ❌ BAD: Sequential async
result1 = await fetch(url1)
result2 = await fetch(url2)
result3 = await fetch(url3)
```

## Testing Recommendations
- Use `pytest` over `unittest` (more Pythonic)
- Mock with `unittest.mock` or `pytest-mock`
- Use `tox` for multi-version testing
- `coverage.py` for coverage reporting
- `hypothesis` for property-based testing

## Type Hints (Python 3.5+)
Encourage type hints for maintainability:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

from typing import List, Optional
def process_items(items: List[int], filter_val: Optional[int] = None) -> List[int]:
    ...
```

Use `mypy` for static type checking.

## Related Security Tasks
- `review-tasks/security/sql-injection.md`
- `review-tasks/security/command-injection.md`
- `review-tasks/security/insecure-deserialization.md`
- `review-tasks/security/path-traversal.md`
- `review-tasks/security/xss.md` (Django/Flask templates)

## Quick Python Security Checklist
- [ ] No `eval()` or `exec()` with user input
- [ ] No `pickle.loads()` on untrusted data
- [ ] Subprocess uses `shell=False` with argument list
- [ ] SQL queries parameterized (no f-strings in queries)
- [ ] Django/Flask templates auto-escape (no `| safe` on user data)
- [ ] File paths canonicalized and validated
- [ ] Secrets from environment variables, not hardcoded
- [ ] Debug mode disabled in production
- [ ] CSRF protection enabled (Django/Flask-WTF)
- [ ] HTTPS enforced for production
