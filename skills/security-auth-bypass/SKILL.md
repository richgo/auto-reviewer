---
name: security auth bypass
description: >
  Authentication/Authorization Bypass. Use this skill
  whenever diffs may introduce security issues on web, api, mobile, especially in all.
  Actively look for: Missing or insufficient authentication/authorization checks
  allowing unauthorized access to resources or actions. Includes broken access control
  (OWASP #1),... and report findings with critical severity expectations and actionable
  fixes.
---

# Authentication/Authorization Bypass
## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `web, api, mobile`
- Languages: `all`

## Purpose
Missing or insufficient authentication/authorization checks allowing unauthorized access to resources or actions. Includes broken access control (OWASP #1), BOLA/IDOR, privilege escalation, and missing auth middleware.

## Detection Heuristics
- API endpoints without auth middleware/decorators
- Object access by user-supplied ID without ownership check
- Role checks missing or using client-side data
- Admin endpoints accessible without privilege verification
- JWT/session validation skipped on sensitive routes

## Eval Cases
### Case 1: IDOR — accessing other users' data
```python
@app.route('/api/invoices/<invoice_id>')
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    return jsonify(invoice.to_dict())
```
**Expected finding:** Critical — IDOR vulnerability. Authenticated user can access any invoice by ID. Add ownership check: `if invoice.user_id != current_user.id: abort(403)`

### Case 2: Missing auth on admin endpoint
```javascript
app.delete('/api/users/:id', async (req, res) => {
  await User.findByIdAndDelete(req.params.id);
  res.json({ success: true });
});
```
**Expected finding:** Critical — No authentication or authorization on user deletion endpoint.

### Case 3: Client-side role check only
```javascript
// Frontend check only — no server-side validation
if (user.role === 'admin') {
  const response = await fetch('/api/admin/settings', {
    method: 'PUT',
    body: JSON.stringify(settings)
  });
}
```
**Expected finding:** High — Authorization check is client-side only. Server endpoint `/api/admin/settings` must validate admin role independently.

## Counter-Examples
### Counter 1: Proper ownership check
```python
@app.route('/api/invoices/<invoice_id>')
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if invoice.user_id != current_user.id:
        abort(403)
    return jsonify(invoice.to_dict())
```
**Why it's correct:** Verifies the requesting user owns the resource.

## Binary Eval Assertions
- [ ] Detects IDOR in eval case 1
- [ ] Detects missing auth in eval case 2
- [ ] Detects client-side-only auth in eval case 3
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes specific fix (ownership check / middleware)
- [ ] Severity assigned as critical
