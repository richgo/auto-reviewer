# Task: Path Traversal

## Category
security

## Severity
critical

## Platforms
web, api

## Languages
all

## Description
User input used to construct file paths without sanitization, allowing attackers to read/write arbitrary files via `../` sequences.

## Detection Heuristics
- File path construction using user input (query params, form data, URL path segments)
- `os.path.join()` or path concatenation with user strings without canonicalization check
- File serve/download endpoints with user-controlled filenames
- Missing check that resolved path is within expected directory

## Eval Cases

### Case 1: Direct path concatenation
```python
@app.route('/files/<filename>')
def serve_file(filename):
    return send_file(f'/uploads/{filename}')
```
**Expected finding:** Critical — Path traversal. `filename` like `../../etc/passwd` escapes upload directory. Use `safe_join()` or validate resolved path starts with `/uploads/`.

### Case 2: Node.js path join
```javascript
app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'files', req.query.name);
  res.sendFile(filePath);
});
```
**Expected finding:** Critical — Path traversal. `path.join` resolves `..` segments. Verify `path.resolve()` output starts with expected base directory.

## Counter-Examples

### Counter 1: Safe join with validation
```python
from werkzeug.utils import safe_join

@app.route('/files/<filename>')
def serve_file(filename):
    filepath = safe_join('/uploads', filename)
    return send_file(filepath)
```
**Why it's correct:** `safe_join` rejects paths that escape the base directory.

## Binary Eval Assertions
- [ ] Detects path traversal in eval case 1
- [ ] Detects path traversal in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding mentions `../` escape risk
- [ ] Finding suggests path validation fix
- [ ] Severity assigned as critical
