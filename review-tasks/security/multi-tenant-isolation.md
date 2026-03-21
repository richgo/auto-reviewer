# Task: Multi-Tenant Isolation Failures

## Category
security

## Severity
critical

## Platforms
all

## Languages
all

## Description
Multi-tenant isolation failures allow one tenant to access another tenant's data through missing tenant ID validation, SQL injection bypassing filters, insecure direct object references, or shared caching/session stores without proper scoping.

## Detection Heuristics
- Database queries missing tenant ID filter
- Tenant context not enforced in ORM/query builder
- Accepting tenant ID from user input without validation
- Shared Redis/cache keys without tenant prefix
- Cross-tenant object references in URLs/APIs
- Missing row-level security (RLS) in database

## Eval Cases

### Case 1: Missing tenant filter in query
```python
# BUGGY CODE — should be detected
@app.route('/api/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.filter_by(id=doc_id).first_or_404()
    # Missing tenant check! Any authenticated user can access any tenant's docs
    return jsonify(doc.to_dict())
```
**Expected finding:** Critical — Missing tenant isolation. User from Tenant A can access Tenant B's document by guessing doc_id. Add tenant filter: `Document.query.filter_by(id=doc_id, tenant_id=current_user.tenant_id)`.

### Case 2: Tenant ID from user input
```javascript
// BUGGY CODE — should be detected
app.get('/api/reports', authenticateUser, async (req, res) => {
  const tenantId = req.query.tenantId; // User-controlled!
  const reports = await db.reports.find({ tenant_id: tenantId });
  res.json(reports);
});
```
**Expected finding:** Critical — Tenant ID accepted from query parameter. User can request any tenant's data by changing `?tenantId=xxx`. Use tenant from authenticated session: `req.user.tenantId`.

### Case 3: Shared cache without tenant scoping
```python
# BUGGY CODE — should be detected
@cache.memoize(timeout=300)
def get_user_settings(user_id):
    return UserSettings.query.filter_by(user_id=user_id).first()

# Cache key: "get_user_settings:123"
# If User 123 exists in multiple tenants, cache collision!
```
**Expected finding:** High — Cache key missing tenant scope. User ID alone is not globally unique across tenants, causing cache pollution. Include tenant in cache key: `@cache.memoize(timeout=300, make_cache_key=lambda user_id: f"{current_tenant_id}:{user_id}")`.

## Counter-Examples

### Counter 1: Tenant-scoped query
```python
# CORRECT CODE — should NOT be flagged
@app.route('/api/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.filter_by(
        id=doc_id,
        tenant_id=current_user.tenant_id
    ).first_or_404()
    return jsonify(doc.to_dict())
```
**Why it's correct:** Query filtered by both doc_id and tenant_id from authenticated session.

### Counter 2: Tenant from session context
```javascript
// CORRECT CODE — should NOT be flagged
app.get('/api/reports', authenticateUser, async (req, res) => {
  const tenantId = req.user.tenantId; // From authenticated JWT
  const reports = await db.reports.find({ tenant_id: tenantId });
  res.json(reports);
});
```
**Why it's correct:** Tenant ID sourced from trusted authentication context, not user input.

## Binary Eval Assertions
- [ ] Detects missing tenant filter in eval case 1
- [ ] Detects tenant ID from input in eval case 2
- [ ] Detects unscoped cache key in eval case 3
- [ ] Does NOT flag counter-example 1 (tenant-scoped query)
- [ ] Does NOT flag counter-example 2 (tenant from session)
- [ ] Finding references OWASP Multi-Tenant Security
- [ ] Severity assigned as critical
