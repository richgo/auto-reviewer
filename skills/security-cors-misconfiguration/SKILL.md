---
name: security cors misconfiguration
description: >
  CORS Misconfiguration. Use this skill whenever diffs
  may introduce security issues on web, api, especially in all. Actively look for: CORS
  (Cross-Origin Resource Sharing) misconfigurations allow unauthorized origins to access
  sensitive resources, leading to data theft or CSRF-like... and report findings with
  medium severity expectations and actionable fixes.
---

# CORS Misconfiguration
## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web, api`
- Languages: `all`

## Purpose
CORS (Cross-Origin Resource Sharing) misconfigurations allow unauthorized origins to access sensitive resources, leading to data theft or CSRF-like attacks. Common issues include wildcard origins, reflecting request origin, and overly permissive headers.

## Detection Heuristics
- Access-Control-Allow-Origin: * with credentials
- Dynamically reflecting Origin header without validation
- Access-Control-Allow-Credentials: true with wildcard origin
- Overly permissive allowed methods (PUT, DELETE for public APIs)
- Missing origin allowlist validation
- CORS enabled on sensitive endpoints (admin, internal APIs)

## Eval Cases
### Case 1: Wildcard origin with credentials
```python
# BUGGY CODE — should be detected
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
```
**Expected finding:** High — CORS wildcard origin with credentials. Browser blocks this (spec violation), but code indicates intent to allow all origins with auth. Use specific origin allowlist instead of *.

### Case 2: Reflecting untrusted origin
```javascript
// BUGGY CODE — should be detected
app.use((req, res, next) => {
  const origin = req.headers.origin;
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  next();
});
```
**Expected finding:** Critical — Unsafe origin reflection. Any origin can access API with credentials, bypassing same-origin policy. Validate origin against allowlist: `['https://app.example.com', 'https://trusted.com']`.

### Case 3: Overly permissive methods on sensitive endpoint
```java
// BUGGY CODE — should be detected
@CrossOrigin(origins = "*", methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.DELETE})
@RestController
public class AdminController {
    @DeleteMapping("/admin/users/{id}")
    public ResponseEntity deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.ok().build();
    }
}
```
**Expected finding:** High — CORS allows DELETE from any origin on admin endpoint. Malicious site can trigger user deletion. Restrict origins to trusted admin domains and require CSRF token for state-changing operations.

## Counter-Examples
### Counter 1: Origin allowlist validation
```python
# CORRECT CODE — should NOT be flagged
ALLOWED_ORIGINS = ['https://app.example.com', 'https://mobile.example.com']

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
```
**Why it's correct:** Origin validated against strict allowlist before setting CORS headers.

### Counter 2: CORS library with configuration
```javascript
// CORRECT CODE — should NOT be flagged
const cors = require('cors');
const corsOptions = {
  origin: ['https://app.example.com', 'https://trusted.com'],
  credentials: true,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
};
app.use(cors(corsOptions));
```
**Why it's correct:** CORS middleware configured with specific origins, limited methods, credentials properly scoped.

## Binary Eval Assertions
- [ ] Detects wildcard with credentials in eval case 1
- [ ] Detects unsafe origin reflection in eval case 2
- [ ] Detects overly permissive methods in eval case 3
- [ ] Does NOT flag counter-example 1 (origin allowlist)
- [ ] Does NOT flag counter-example 2 (CORS library with config)
- [ ] Finding references OWASP CORS Security Cheat Sheet
- [ ] Severity assigned as medium to high based on endpoint sensitivity
