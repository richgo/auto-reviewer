# Task: Cookie Security Flaws

## Category
security

## Severity
high

## Platforms
web

## Languages
all

## Description
Cookie security flaws include missing Secure, HttpOnly, and SameSite flags, overly broad domain/path scope, excessive expiration times, and sensitive data stored in cookies without encryption or integrity protection.

## Detection Heuristics
- Session/auth cookies missing Secure flag (allows HTTP transmission)
- Missing HttpOnly flag (accessible via JavaScript, XSS risk)
- Missing SameSite attribute (CSRF vulnerable)
- Domain set to parent domain (.example.com) instead of specific subdomain
- Path set to / when narrower scope is appropriate
- Expiration > 1 year for session cookies
- Sensitive PII stored in plaintext cookies

## Eval Cases

### Case 1: Auth cookie missing security flags
```python
# BUGGY CODE — should be detected
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('session_id', user.session_token)
        return resp
```
**Expected finding:** High — Session cookie missing security flags. Cookie lacks Secure (HTTPS-only), HttpOnly (XSS protection), and SameSite (CSRF protection). Add: `resp.set_cookie('session_id', token, secure=True, httponly=True, samesite='Strict')`.

### Case 2: Sensitive data in cookie
```javascript
// BUGGY CODE — should be detected
app.post('/checkout', (req, res) => {
  const userData = {
    email: req.body.email,
    creditCard: req.body.card,
    ssn: req.body.ssn
  };
  res.cookie('checkout_data', JSON.stringify(userData));
  res.redirect('/confirm');
});
```
**Expected finding:** Critical — Sensitive PII (credit card, SSN) stored in plaintext cookie. Cookies transmitted with every request, logged by proxies, and accessible client-side. Store in encrypted server-side session with only session ID in cookie.

### Case 3: Overly broad cookie scope
```java
// BUGGY CODE — should be detected
Cookie authCookie = new Cookie("auth_token", token);
authCookie.setDomain(".example.com"); // Applies to all subdomains
authCookie.setPath("/");
authCookie.setMaxAge(365 * 24 * 60 * 60); // 1 year
response.addCookie(authCookie);
```
**Expected finding:** High — Overly broad cookie scope and excessive expiration. Cookie sent to all subdomains (including potentially compromised ones), valid for 1 year. Restrict to specific subdomain, use narrower path, set shorter expiration (session or < 30 days).

## Counter-Examples

### Counter 1: Secure cookie configuration
```python
# CORRECT CODE — should NOT be flagged
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie(
            'session_id',
            user.session_token,
            secure=True,
            httponly=True,
            samesite='Strict',
            max_age=1800  # 30 minutes
        )
        return resp
```
**Why it's correct:** All security flags set, reasonable expiration.

### Counter 2: Server-side session storage
```javascript
// CORRECT CODE — should NOT be flagged
app.post('/checkout', (req, res) => {
  req.session.checkoutData = {
    email: req.body.email,
    // Sensitive data in server-side session
  };
  res.redirect('/confirm');
});
```
**Why it's correct:** Sensitive data stored server-side, only session ID in cookie (managed by express-session with security defaults).

## Binary Eval Assertions
- [ ] Detects missing cookie flags in eval case 1
- [ ] Detects sensitive data in cookie in eval case 2
- [ ] Detects broad scope/long expiration in eval case 3
- [ ] Does NOT flag counter-example 1 (secure flags set)
- [ ] Does NOT flag counter-example 2 (server-side storage)
- [ ] Finding lists all three flags: Secure, HttpOnly, SameSite
- [ ] Severity assigned as high or critical for auth cookies
