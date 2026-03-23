---
name: security rest security
description: >
  Migrated review-task skill for REST API Security Issues. Use this skill whenever diffs
  may introduce security issues on web, api, especially in all. Actively look for: REST
  API security issues include excessive data exposure, lack of rate limiting, missing
  authentication on endpoints, verbose error... and report findings with medium severity
  expectations and actionable fixes.
---

# REST API Security Issues

## Source Lineage
- Original review task: `review-tasks/security/rest-security.md`
- Migrated skill artifact: `skills/review-task-security-rest-security/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web, api`
- Languages: `all`

## Purpose
REST API security issues include excessive data exposure, lack of rate limiting, missing authentication on endpoints, verbose error messages leaking implementation details, and improper HTTP method restrictions.

## Detection Heuristics
- API endpoints returning full database models instead of filtered DTOs
- No rate limiting on public endpoints
- Missing authentication middleware on sensitive routes
- Error responses exposing stack traces or SQL queries
- Accepting unauthorized HTTP methods (PUT/DELETE on read-only resources)
- No pagination on list endpoints (allows data scraping)

## Eval Cases
### Case 1: Excessive data exposure
```python
# BUGGY CODE — should be detected
@app.route('/api/users/<id>')
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.__dict__) # Exposes all fields including password hash!
```
**Expected finding:** High — Excessive data exposure. API returns all user fields including password_hash, internal IDs. Use DTO/serializer to expose only safe fields: `{id, username, email}`.

### Case 2: No rate limiting
```javascript
// BUGGY CODE — should be detected
app.post('/api/auth/login', async (req, res) => {
  const user = await User.authenticate(req.body.username, req.body.password);
  if (user) {
    res.json({ token: user.generateToken() });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});
```
**Expected finding:** High — No rate limiting on login endpoint. Allows unlimited brute-force attempts. Add rate limiting: `rateLimit({ windowMs: 15 * 60 * 1000, max: 5 })`.

### Case 3: Verbose error messages
```java
// BUGGY CODE — should be detected
@GetMapping("/api/orders/{id}")
public ResponseEntity getOrder(@PathVariable Long id) {
    try {
        Order order = orderRepository.findById(id).orElseThrow();
        return ResponseEntity.ok(order);
    } catch (Exception e) {
        return ResponseEntity.status(500).body(e.getMessage() + "\n" + e.getStackTrace());
    }
}
```
**Expected finding:** Medium — Verbose error message exposes stack trace. Reveals implementation details (ORM, file paths, dependencies) aiding attackers. Return generic error in production, log details server-side.

## Counter-Examples
### Counter 1: DTO for data filtering
```python
# CORRECT CODE — should NOT be flagged
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()

user_schema = UserSchema()

@app.route('/api/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))
```
**Why it's correct:** Marshmallow schema exposes only safe fields, excludes password_hash.

### Counter 2: Rate limiting with express-rate-limit
```javascript
// CORRECT CODE — should NOT be flagged
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, try again later'
});

app.post('/api/auth/login', loginLimiter, async (req, res) => {
  // ... authentication logic
});
```
**Why it's correct:** Rate limiting prevents brute-force attacks (5 attempts per 15 min).

## Binary Eval Assertions
- [ ] Detects excessive data exposure in eval case 1
- [ ] Detects missing rate limiting in eval case 2
- [ ] Detects verbose errors in eval case 3
- [ ] Does NOT flag counter-example 1 (DTO filtering)
- [ ] Does NOT flag counter-example 2 (rate limiting)
- [ ] Finding references OWASP REST Security Cheat Sheet
- [ ] Severity assigned as medium to high based on exposure

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
