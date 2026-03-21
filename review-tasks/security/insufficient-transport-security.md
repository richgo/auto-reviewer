# Task: Insufficient Transport Layer Security

## Category
security

## Severity
high

## Platforms
web, api, mobile

## Languages
all

## Description
Insufficient transport security includes accepting unencrypted HTTP connections, weak TLS versions (< 1.2), insecure cipher suites, missing certificate validation, and failure to enforce HTTPS for sensitive data transmission.

## Detection Heuristics
- HTTP URLs for sensitive endpoints (login, payments, API keys)
- TLS version < 1.2 allowed (SSLv3, TLS 1.0/1.1 deprecated)
- Weak cipher suites: RC4, DES, export ciphers, CBC without AEAD
- Missing HSTS (HTTP Strict Transport Security) header
- Certificate validation disabled in HTTP clients
- Mixed content (HTTPS page loading HTTP resources)

## Eval Cases

### Case 1: HTTP client disabling certificate validation
```python
# BUGGY CODE — should be detected
import requests
response = requests.get('https://api.example.com/data', verify=False)
```
**Expected finding:** Critical — SSL certificate validation disabled. Application vulnerable to man-in-the-middle attacks. Remove `verify=False` or provide custom CA bundle if needed for internal CAs.

### Case 2: Missing HSTS header
```javascript
// BUGGY CODE — should be detected
const express = require('express');
const https = require('https');
const app = express();

app.get('/', (req, res) => {
  res.send('Secure content');
});

https.createServer(options, app).listen(443);
```
**Expected finding:** High — Missing HTTP Strict Transport Security header. Browser may allow downgrade to HTTP, enabling MitM. Add middleware: `app.use((req, res, next) => { res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains'); next(); })`.

### Case 3: Accepting TLS 1.0/1.1
```java
// BUGGY CODE — should be detected
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, null, null); // Allows all TLS versions including deprecated
SSLSocketFactory socketFactory = sslContext.getSocketFactory();
```
**Expected finding:** High — Weak TLS versions accepted (1.0/1.1). Vulnerable to BEAST, POODLE attacks. Enforce TLS 1.2+: `SSLContext.getInstance("TLSv1.2")` or `SSLContext.getInstance("TLS")` with explicit protocol restriction.

## Counter-Examples

### Counter 1: Proper certificate validation
```python
# CORRECT CODE — should NOT be flagged
import requests
response = requests.get('https://api.example.com/data')
# verify=True by default, validates certificates
```
**Why it's correct:** Certificate validation enabled (default behavior).

### Counter 2: HSTS with preload
```javascript
// CORRECT CODE — should NOT be flagged
const helmet = require('helmet');
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```
**Why it's correct:** HSTS enforced with 1-year max-age, subdomain coverage, preload-ready.

## Binary Eval Assertions
- [ ] Detects disabled certificate validation in eval case 1
- [ ] Detects missing HSTS in eval case 2
- [ ] Detects weak TLS versions in eval case 3
- [ ] Does NOT flag counter-example 1 (proper validation)
- [ ] Does NOT flag counter-example 2 (HSTS enabled)
- [ ] Finding references OWASP Transport Layer Protection Cheat Sheet
- [ ] Severity assigned as high or critical for disabled cert validation
