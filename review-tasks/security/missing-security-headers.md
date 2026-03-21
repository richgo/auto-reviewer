# Task: Missing Security Headers

## Category
security

## Severity
medium

## Platforms
web

## Languages
all

## Description
Missing security headers leave web applications vulnerable to XSS, clickjacking, MIME sniffing, and other client-side attacks. Critical headers include CSP, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy.

## Detection Heuristics
- Missing Content-Security-Policy header
- Missing X-Frame-Options or frame-ancestors CSP directive
- Missing X-Content-Type-Options: nosniff
- Missing Referrer-Policy (leaks sensitive URL parameters)
- Permissive Permissions-Policy (formerly Feature-Policy)
- Missing Cross-Origin headers (CORP, COOP, COEP) for resource isolation

## Eval Cases

### Case 1: No Content-Security-Policy
```python
# BUGGY CODE — should be detected
@app.route('/')
def index():
    return render_template('index.html')
# No CSP header set
```
**Expected finding:** Medium — Missing Content-Security-Policy header. No protection against XSS via inline scripts or unauthorized third-party scripts. Add CSP: `default-src 'self'; script-src 'self'; object-src 'none'`.

### Case 2: Missing X-Frame-Options
```javascript
// BUGGY CODE — should be detected
app.get('/', (req, res) => {
  res.send('<html><body>Sensitive content</body></html>');
});
```
**Expected finding:** Medium — Missing X-Frame-Options header. Page can be embedded in iframe, vulnerable to clickjacking attacks. Set `X-Frame-Options: DENY` or use CSP `frame-ancestors 'none'`.

### Case 3: Missing X-Content-Type-Options
```java
// BUGGY CODE — should be detected
@GetMapping("/api/data")
public ResponseEntity<String> getData() {
    return ResponseEntity.ok()
        .body("{\"data\": \"value\"}");
}
```
**Expected finding:** Medium — Missing X-Content-Type-Options: nosniff. Browser may MIME-sniff responses as executable, enabling XSS if user-controlled content is served. Add header to all responses.

## Counter-Examples

### Counter 1: Comprehensive security headers with Helmet
```javascript
// CORRECT CODE — should NOT be flagged
const helmet = require('helmet');
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: []
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true
  }
}));
```
**Why it's correct:** Helmet sets CSP, HSTS, X-Frame-Options, X-Content-Type-Options, and other security headers.

### Counter 2: Django security middleware
```python
# CORRECT CODE — should NOT be flagged
# settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
```
**Why it's correct:** Django security settings enforce X-Content-Type-Options, X-Frame-Options, CSP.

## Binary Eval Assertions
- [ ] Detects missing CSP in eval case 1
- [ ] Detects missing X-Frame-Options in eval case 2
- [ ] Detects missing X-Content-Type-Options in eval case 3
- [ ] Does NOT flag counter-example 1 (Helmet with CSP)
- [ ] Does NOT flag counter-example 2 (Django security settings)
- [ ] Finding lists recommended header values
- [ ] Severity assigned as medium (or high if CSP missing on auth pages)
