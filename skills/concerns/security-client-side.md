---
name: security-client-side
description: >
  Detect client-side security vulnerabilities: cookie security issues, clickjacking, prototype
  pollution, third-party code risks, CSP bypass, postMessage validation, client-side storage
  issues, HTML injection, and subresource integrity. Trigger when reviewing browser-based code,
  JavaScript/TypeScript, React/Vue/Angular, or any web frontend with cookies, iframes, or
  third-party dependencies.
---

# Security Review: Client-Side Vulnerabilities

## Purpose
Review client-side code for security issues specific to browser environments: cookie handling, frame security, JavaScript prototype chain manipulation, third-party code integration, Content Security Policy bypass, postMessage origin validation, client-side storage of sensitive data, HTML injection, and CDN/script integrity.

## Scope
This skill covers nine client-side security classes:
1. **Cookie Security** — missing Secure/HttpOnly/SameSite flags
2. **Clickjacking** — missing X-Frame-Options/CSP frame-ancestors
3. **Prototype Pollution** — user input modifying Object.prototype
4. **Third-Party Code** — unvalidated CDN scripts, supply chain attacks
5. **CSP Bypass** — unsafe-inline, unsafe-eval, weak nonces
6. **postMessage Validation** — missing origin checks, window.opener attacks
7. **Client-Side Storage** — tokens/secrets in localStorage/IndexedDB
8. **HTML Injection** — user content in meta tags, link injection
9. **Subresource Integrity** — CDN scripts without SRI hashes

## Detection Strategy

### 1. Cookie Security Red Flags
- `Set-Cookie` without `Secure` flag (allows HTTP transmission)
- Missing `HttpOnly` flag (accessible to JavaScript)
- Missing or weak `SameSite` attribute (CSRF risk)
- Session cookie with long expiration
- Sensitive data in cookie value (not encrypted)

**High-risk patterns:**
```javascript
// ❌ UNSAFE
document.cookie = `session=${token}`;
response.cookie('auth', token);
Set-Cookie: session=abc123
```

### 2. Clickjacking Red Flags
- No `X-Frame-Options` header
- No `frame-ancestors` CSP directive
- `X-Frame-Options: ALLOW-FROM` (deprecated, not supported in modern browsers)

**High-risk patterns:**
```javascript
// ❌ Missing frame protection
app.use((req, res, next) => { next(); });
```

### 3. Prototype Pollution Red Flags
- Object merge without prototype check
- Deep object assignment from user input
- Missing `Object.hasOwnProperty` check
- `JSON.parse` → `Object.assign` on user data

**High-risk patterns:**
```javascript
// ❌ UNSAFE
Object.assign({}, userInput);
merge(config, req.body);
_.merge(target, untrustedSource);
```

### 4. Third-Party Code Red Flags
- Inline script from CDN without SRI
- Dynamic script insertion from user-controlled URLs
- Loading scripts from HTTP (not HTTPS)
- Webpack externals from untrusted sources

**High-risk patterns:**
```html
<!-- ❌ UNSAFE -->
<script src="https://cdn.example.com/lib.js"></script>
<script src="${userProvidedUrl}"></script>
```

### 5. CSP Bypass Red Flags
- `unsafe-inline` or `unsafe-eval` in CSP
- Nonce not cryptographically random or reused
- `script-src *` wildcard
- CSP set via meta tag (weaker than header)

**High-risk patterns:**
```html
<meta http-equiv="Content-Security-Policy" 
      content="script-src 'unsafe-inline';">
```

### 6. postMessage Validation Red Flags
- `window.addEventListener('message')` without origin check
- `event.origin === '*'` check
- `postMessage(data, '*')` to any origin
- Trusting `window.opener` data without validation

**High-risk patterns:**
```javascript
// ❌ UNSAFE
window.addEventListener('message', (event) => {
  eval(event.data);
});
```

### 7. Client-Side Storage Red Flags
- JWT/API tokens in `localStorage`
- Sensitive data in `sessionStorage` (still accessible to XSS)
- Unencrypted PII in IndexedDB
- Secrets in `window.name`

**High-risk patterns:**
```javascript
// ❌ UNSAFE
localStorage.setItem('authToken', jwt);
sessionStorage.setItem('ssn', user.ssn);
```

### 8. HTML Injection Red Flags
- User input in `<meta>` tags (open redirect, CSP bypass)
- User input in `<link rel="canonical">` (SEO poisoning)
- Form action hijacking: `<form action="${userInput}">`
- User input in `<base href>` (script base hijacking)

**High-risk patterns:**
```html
<!-- ❌ UNSAFE -->
<meta property="og:url" content="${req.query.url}">
<link rel="canonical" href="${userCanonical}">
```

### 9. Subresource Integrity Red Flags
- External scripts without `integrity` attribute
- CDN fallback without SRI check
- SRI hash not using SHA-384 or SHA-512

**High-risk patterns:**
```html
<!-- ❌ UNSAFE -->
<script src="https://cdn.example.com/jquery.min.js"></script>
```

## Platform-Specific Guidance

### Web/Browser
- **Primary risks:** Cookie security, XSS via client-side storage, clickjacking, prototype pollution
- **Key review areas:** Cookie middleware, postMessage handlers, merge utilities, CSP headers
- **OWASP references:** Cookie_Theft_Mitigation, Clickjacking_Defense, Prototype_Pollution_Prevention, Third_Party_Javascript_Management

### React/Vue/Angular
- **Primary risks:** Prototype pollution from state management, postMessage in micro-frontends, CSP with inline styles
- **Extra checks:** Zustand/Redux merge logic, iframe communication in module federation, unsafe dangerouslySetInnerHTML

### Mobile Web/PWA
- **Primary risks:** Service worker script injection, manifest.json manipulation, cache poisoning
- **Extra checks:** Service worker fetch handlers, Web App Manifest integrity, push notification payload validation

## Review Instructions

### Step 1: Check Cookie Configuration
Scan for `Set-Cookie`, `res.cookie()`, `document.cookie`:
1. **Secure flag:** Must be present for HTTPS sites
2. **HttpOnly:** Required for session/auth cookies
3. **SameSite:** Strict or Lax (not None without Secure)
4. **Expiration:** Session cookies should not set Max-Age > 1 day

### Step 2: Verify Frame Protection
Check HTTP response headers or meta tags:
1. **X-Frame-Options:** Should be `DENY` or `SAMEORIGIN`
2. **CSP frame-ancestors:** Preferred over X-Frame-Options
3. **Absence of both:** Flag as clickjacking risk

### Step 3: Scan for Prototype Pollution
Search for:
- `Object.assign`, `_.merge`, `$.extend` with user input
- Deep merge utilities without prototype checks
- `JSON.parse` → object spread on untrusted data

**Safe pattern:** Use `Object.create(null)` for user-controlled objects.

### Step 4: Validate Third-Party Scripts
For each `<script src>`:
1. **SRI present:** Check for `integrity="sha384-..."`
2. **HTTPS:** All scripts must use HTTPS
3. **Known CDN:** Verify CDN is reputable (jsdelivr, unpkg, cdnjs)
4. **Version pinning:** Scripts should pin exact version, not `@latest`

### Step 5: Review CSP Policy
Extract CSP from headers or meta tag:
1. **No unsafe-inline/unsafe-eval:** Unless nonce-based
2. **Nonce entropy:** Ensure cryptographically random
3. **Whitelist domains:** Avoid wildcards in script-src
4. **Upgrade-insecure-requests:** Should be present for HTTPS sites

### Step 6: Audit postMessage Handlers
For each `window.addEventListener('message')`:
1. **Origin validation:** Must check `event.origin` against whitelist
2. **Data sanitization:** Never `eval()` or `innerHTML` message data
3. **Targeted sending:** `postMessage(data, specificOrigin)`, not `'*'`

### Step 7: Inspect Client-Side Storage
Scan for `localStorage`, `sessionStorage`, `indexedDB`:
1. **No tokens:** JWT/API keys should be in httpOnly cookies
2. **No PII:** Encrypt sensitive data client-side if storage required
3. **Expiration:** Implement expiration for cached data

### Step 8: Detect HTML Injection Points
Check for user input in:
- `<meta>` tags (og:url, canonical, description)
- `<link>` tags (canonical, alternate)
- `<form action>`
- `<base href>`

**Fix:** Validate URLs against allowlist, use relative URLs where possible.

### Step 9: Verify Subresource Integrity
For all external scripts/styles:
1. **Generate SRI:** `openssl dgst -sha384 -binary file.js | openssl base64 -A`
2. **Add integrity attribute:** `integrity="sha384-..."`
3. **Add crossorigin:** `crossorigin="anonymous"` for CORS resources

## Examples

### ✅ SAFE: Secure Cookie
```javascript
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000 // 1 hour
});
```

### ❌ UNSAFE: Insecure Cookie
```javascript
res.cookie('session', token);
```
**Finding:** High — Missing HttpOnly, Secure, SameSite flags. Cookie vulnerable to XSS theft and CSRF.

### ✅ SAFE: Frame Protection
```javascript
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Content-Security-Policy', "frame-ancestors 'none'");
  next();
});
```

### ❌ UNSAFE: No Frame Protection
```javascript
app.use((req, res, next) => { next(); });
```
**Finding:** Medium — Missing X-Frame-Options. Application vulnerable to clickjacking.

### ✅ SAFE: Prototype Pollution Prevention
```javascript
function merge(target, source) {
  for (const key in source) {
    if (Object.hasOwnProperty.call(source, key) &&
        !['__proto__', 'constructor', 'prototype'].includes(key)) {
      target[key] = source[key];
    }
  }
}
```

### ❌ UNSAFE: Prototype Pollution
```javascript
Object.assign(config, req.body);
```
**Finding:** High — Prototype pollution via Object.assign. Attacker can inject `__proto__` to pollute Object.prototype.

### ✅ SAFE: SRI for CDN Script
```html
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"
        integrity="sha384-3BvMrx4N4k+CQcdM/0V7ELF2B3l0JxFPkuY3rBSsN/p1K6vHfV3E7BQKDjLLl+O+"
        crossorigin="anonymous"></script>
```

### ❌ UNSAFE: CDN Script Without SRI
```html
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"></script>
```
**Finding:** Medium — Missing SRI hash. CDN compromise could inject malicious code.

### ✅ SAFE: postMessage with Origin Check
```javascript
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted.example.com') {
    return;
  }
  processMessage(event.data);
});
```

### ❌ UNSAFE: postMessage Without Origin Check
```javascript
window.addEventListener('message', (event) => {
  eval(event.data);
});
```
**Finding:** Critical — postMessage without origin validation + eval(). Attacker can execute arbitrary JavaScript.

### ✅ SAFE: Token in httpOnly Cookie
```javascript
// Server-side
res.cookie('token', jwt, { httpOnly: true, secure: true });
```

### ❌ UNSAFE: Token in localStorage
```javascript
localStorage.setItem('authToken', jwt);
```
**Finding:** High — JWT in localStorage. Accessible to XSS attacks. Use httpOnly cookie instead.

## Migration Coverage
Review guidance from the legacy review-task corpus is now consolidated in this skill and validated via the migration inventory (`openspec/changes/research-changes/artifacts/review-task-skill-map.csv`).

## OWASP References
- [Cookie Theft Mitigation](https://cheatsheetseries.owasp.org/cheatsheets/Cookie_Theft_Mitigation_Cheat_Sheet.html)
- [Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html)
- [Prototype Pollution Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html)
- [Third Party Javascript Management](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)
- [Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)

## Quick Checklist
- [ ] All cookies have Secure, HttpOnly, SameSite flags
- [ ] X-Frame-Options or CSP frame-ancestors set
- [ ] No prototype pollution in merge/assign operations
- [ ] All external scripts have SRI hashes
- [ ] CSP policy without unsafe-inline/unsafe-eval
- [ ] postMessage handlers validate event.origin
- [ ] No tokens/secrets in localStorage/sessionStorage
- [ ] User input in meta/link tags validated
- [ ] CDN scripts use HTTPS with pinned versions
