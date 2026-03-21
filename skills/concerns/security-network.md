---
name: security-network
description: >
  Detect network security vulnerabilities: SSRF, insufficient transport security, missing security
  headers, CORS misconfiguration, and open redirects. Trigger when reviewing HTTP request handling,
  redirect logic, response headers, URL validation, or any code making outbound requests.
---

# Security Review: Network & Transport Security

## Purpose
Review code for network-layer vulnerabilities that expose applications to SSRF attacks, man-in-the-middle attacks, clickjacking, or allow unauthorized cross-origin access.

## Scope
Five network security vulnerability classes:
1. **SSRF (Server-Side Request Forgery)** — application makes requests to attacker-controlled URLs
2. **Insufficient Transport Security** — missing HTTPS, weak TLS configuration
3. **Missing Security Headers** — no CSP, HSTS, X-Frame-Options, etc.
4. **CORS Misconfiguration** — overly permissive Access-Control-Allow-Origin
5. **Open Redirect** — unvalidated redirects to external sites

## Detection Strategy

### Universal Red Flags
- **User-controlled URLs** in outbound HTTP requests
- **HTTP (not HTTPS)** for sensitive operations
- **Missing security headers** in HTTP responses
- **Wildcard CORS** (`Access-Control-Allow-Origin: *`)
- **Unvalidated redirect targets**

### High-Risk Patterns

**SSRF:**
- `requests.get(user_url)`
- `fetch(req.query.url)`
- `URL.openConnection(userProvidedURL)`
- Webhook URLs not validated
- PDF generators with HTML input (can load external resources)

**Insufficient Transport Security:**
- `http://` URLs for auth, payment, PII
- `requests.get(url, verify=False)` (disables cert validation)
- `NODE_TLS_REJECT_UNAUTHORIZED=0`
- Outdated TLS versions (1.0, 1.1)

**Missing Security Headers:**
- No `Content-Security-Policy`
- No `X-Frame-Options` or `frame-ancestors`
- No `Strict-Transport-Security` (HSTS)
- No `X-Content-Type-Options: nosniff`

**CORS Misconfiguration:**
- `Access-Control-Allow-Origin: *` with credentials
- `Access-Control-Allow-Origin: ${req.headers.origin}` (reflects origin)
- Missing origin allowlist validation

**Open Redirect:**
- `redirect(request.args.get('next'))`
- `res.redirect(req.query.url)`
- No allowlist or domain validation

## Platform-Specific Guidance

### Web/API
- **Primary risks:** All network security classes listed
- **Key review areas:** HTTP response headers, redirect handlers, outbound request logic, CORS middleware
- **OWASP references:** SSRF_Prevention, Transport_Layer_Security, HTTP_Headers

### Android
- **Primary risks:** Cleartext traffic, certificate validation bypass, SSRF via WebView
- **Key review areas:** `network_security_config.xml`, `setHostnameVerifier`, `WebView.loadUrl(userInput)`
- **Extra checks:** `usesCleartextTraffic=true`, custom TrustManager

### iOS
- **Primary risks:** ATS bypass, certificate validation bypass, SSRF via WKWebView
- **Key review areas:** `NSAppTransportSecurity`, `URLSession` delegate, `WKWebView.load(URLRequest(url: userURL))`
- **Extra checks:** `NSAllowsArbitraryLoads`, custom certificate validation

### Microservices
- **Primary risks:** SSRF between services, missing mTLS, insecure service-to-service comms
- **Key review areas:** Service mesh TLS config, internal HTTP requests, egress policies
- **Extra checks:** Metadata service SSRF (169.254.169.254), container escape via SSRF

## Review Instructions

### Step 1: Identify Outbound Requests
Find all HTTP client usage:
- `requests`, `urllib`, `httpx` (Python)
- `fetch`, `axios`, `http` (Node.js)
- `HttpClient`, `OkHttp` (Java/Kotlin)
- `URLSession`, `Alamofire` (Swift)

### Step 2: Check URL Validation
For each outbound request:
1. **Source:** Is URL user-controlled?
2. **Allowlist:** Is domain validated against allowlist?
3. **Protocol:** Only http/https allowed (block file://, gopher://, etc.)
4. **Internal IPs:** Block private ranges (127.0.0.1, 169.254.x.x, 10.x.x.x, etc.)

### Step 3: Review TLS Configuration
- **Enforce HTTPS** for sensitive operations
- **Certificate validation enabled** (don't disable `verify`)
- **Minimum TLS 1.2** (1.3 preferred)
- **No hardcoded certificates** (certificate pinning should use proper API)

### Step 4: Check Response Headers
Every HTTP response should have:
- `Content-Security-Policy: ...` (appropriate for app)
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`

### Step 5: Validate CORS Configuration
- **Never:** `Access-Control-Allow-Origin: *` with credentials
- **Allowlist origins:** Validate `req.headers.origin` against allowlist
- **Credentials:** Only set `Access-Control-Allow-Credentials: true` if necessary

### Step 6: Review Redirects
For `redirect(url)` or `Location:` headers:
1. **Validate domain:** Allowlist of permitted redirect targets
2. **Relative paths preferred:** Use `/path` instead of full URL
3. **No open redirects:** Never `redirect(req.query.next)` without validation

### Step 7: Report Findings
For each vulnerability:
- **Severity:** Critical (SSRF), High (TLS bypass, open redirect), Medium (missing headers, CORS)
- **Location:** File, line, function
- **Description:** Attack vector
- **Fix:** Code example with validation/headers

## Examples

### ✅ SAFE: URL Allowlist Validation
```python
ALLOWED_DOMAINS = ['example.com', 'api.example.com']
parsed = urlparse(user_url)
if parsed.hostname not in ALLOWED_DOMAINS:
    abort(400)
response = requests.get(user_url)
```

### ❌ UNSAFE: SSRF
```python
url = request.args.get('url')
response = requests.get(url)
```
**Finding:** Critical — SSRF. Attacker can access internal services (169.254.169.254, localhost).

### ✅ SAFE: Security Headers (Flask)
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### ❌ UNSAFE: Missing Security Headers
```python
return render_template('index.html')
```
**Finding:** Medium — Missing security headers. Add CSP, X-Frame-Options, HSTS.

### ✅ SAFE: CORS with Allowlist
```javascript
const ALLOWED_ORIGINS = ['https://example.com', 'https://app.example.com'];
app.use(cors({
  origin: (origin, callback) => {
    if (ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed'));
    }
  }
}));
```

### ❌ UNSAFE: CORS Wildcard
```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
res.setHeader('Access-Control-Allow-Credentials', 'true');
```
**Finding:** High — Insecure CORS. Wildcard origin with credentials enables CSRF.

### ✅ SAFE: Validated Redirect
```python
ALLOWED_PATHS = ['/dashboard', '/profile', '/settings']
next_url = request.args.get('next', '/')
if next_url not in ALLOWED_PATHS:
    next_url = '/'
return redirect(next_url)
```

### ❌ UNSAFE: Open Redirect
```python
return redirect(request.args.get('next'))
```
**Finding:** High — Open redirect. Attacker can redirect to phishing site.

## Related Review Tasks
- `review-tasks/security/ssrf.md`
- `review-tasks/security/insufficient-transport-security.md`
- `review-tasks/security/missing-security-headers.md`
- `review-tasks/security/cors-misconfiguration.md`
- `review-tasks/security/open-redirect.md`

## OWASP References
- [SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Transport Layer Security](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [Unvalidated Redirects](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)

## Quick Checklist
- [ ] User-controlled URLs validated against allowlist
- [ ] Private IP ranges blocked (127.0.0.1, 169.254.x.x, 10.x.x.x)
- [ ] TLS certificate validation enabled
- [ ] HTTPS enforced for sensitive operations
- [ ] Security headers present (CSP, X-Frame-Options, HSTS)
- [ ] CORS origin allowlist validated
- [ ] Redirects validated against allowlist
- [ ] No `Access-Control-Allow-Origin: *` with credentials
