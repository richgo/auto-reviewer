# Task: Cross-Site Request Forgery (CSRF)

## Category
security

## Severity
high

## Platforms
web

## Languages
all

## Description
State-changing endpoints that accept requests without verifying the request originated from the application, allowing attackers to trick authenticated users into performing unintended actions.

## Detection Heuristics
- POST/PUT/DELETE endpoints without CSRF token validation
- CSRF middleware explicitly disabled or excluded for routes
- Cookie-based auth without SameSite attribute
- State-changing operations on GET endpoints

## Eval Cases

### Case 1: CSRF protection disabled
```python
app = Flask(__name__)
# CSRFProtect not initialized

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    amount = request.form['amount']
    to_account = request.form['to']
    execute_transfer(current_user, to_account, amount)
    return redirect('/dashboard')
```
**Expected finding:** High — No CSRF protection on state-changing endpoint. Initialize `CSRFProtect(app)` and include CSRF tokens in forms.

### Case 2: State change on GET
```javascript
app.get('/api/users/:id/promote', authMiddleware, async (req, res) => {
  await User.findByIdAndUpdate(req.params.id, { role: 'admin' });
  res.json({ success: true });
});
```
**Expected finding:** High — State-changing action (role promotion) on GET endpoint. Use POST/PUT and add CSRF protection.

## Counter-Examples

### Counter 1: CSRF token validated
```python
csrf = CSRFProtect(app)

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    # CSRF token auto-validated by CSRFProtect
    execute_transfer(current_user, request.form['to'], request.form['amount'])
    return redirect('/dashboard')
```
**Why it's correct:** CSRF middleware validates token on every POST.

## Binary Eval Assertions
- [ ] Detects missing CSRF in eval case 1
- [ ] Detects state-change on GET in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes CSRF token remediation
- [ ] Severity assigned as high
