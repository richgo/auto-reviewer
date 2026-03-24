---
name: security auth
description: >
  Detect authentication and authorization vulnerabilities: auth bypass, CSRF, broken authentication,
  session management flaws, credential stuffing weaknesses, insecure password storage/reset, and
  OAuth misconfiguration. Trigger when reviewing login flows, session handling, password operations,
  auth middleware, permission checks, or OAuth/SAML integration.
---

# Security Review: Authentication & Authorization

## Purpose
Review code for authentication and authorization vulnerabilities that allow attackers to bypass access controls, hijack sessions, or compromise user accounts.

## Scope
Eight critical auth-related vulnerability classes:
1. **Auth Bypass** — missing or bypassable permission checks
2. **CSRF** — state-changing operations without anti-CSRF tokens
3. **Authentication Flaws** — weak credential validation, enumeration
4. **Session Management** — insecure session tokens, fixation, hijacking
5. **Credential Stuffing** — missing rate limiting, bot protection
6. **Password Storage** — plaintext/weak hashing, no salts
7. **Password Reset Flaws** — predictable tokens, account takeover
8. **OAuth Misconfiguration** — PKCE missing, redirect_uri validation gaps

## Detection Strategy

### Universal Red Flags
- **Missing auth checks** before sensitive operations
- **Inconsistent enforcement** of permissions across endpoints
- **Client-side only** validation (e.g., hiding UI elements but not enforcing backend)
- **Predictable tokens** or insufficient entropy
- **HTTP instead of HTTPS** for credentials
- **Hardcoded credentials** or secrets in code

### High-Risk Patterns

**Auth Bypass:**
- Direct object reference without ownership check: `SELECT * FROM orders WHERE id = ${req.params.id}`
- Missing `@require_auth` or `@login_required` decorator
- Role check after operation instead of before
- `if user.is_admin` but `user` is client-controlled

**CSRF:**
- State-changing POST/PUT/DELETE without CSRF token validation
- Cookie-based auth without `SameSite` attribute
- Missing `X-CSRF-Token` header validation
- GET requests that mutate state (anti-pattern)

**Authentication Flaws:**
- Username enumeration via error messages
- No account lockout after failed attempts
- Weak password requirements
- Missing MFA for sensitive accounts

**Session Management:**
- Session IDs in URL parameters
- No `HttpOnly`, `Secure`, `SameSite` flags on session cookies
- Session fixation (not regenerating ID after login)
- No session expiry or logout mechanism

**Credential Stuffing:**
- No rate limiting on `/login` endpoint
- Missing CAPTCHA on repeated failures
- No IP-based throttling

**Password Storage:**
- `bcrypt`/`scrypt`/`argon2` NOT used
- MD5/SHA1/SHA256 used for password hashing
- Passwords stored in plaintext or reversibly encrypted

**Password Reset:**
- Reset token sent via GET parameter (leaks in Referer header)
- Token never expires
- Token predictable (sequential, timestamp-based)
- No email confirmation before reset

**OAuth Misconfiguration:**
- `redirect_uri` not validated (open redirect)
- Missing PKCE for public clients (mobile apps)
- `state` parameter not used (CSRF in OAuth flow)
- JWT signature not verified

## Platform-Specific Guidance

### Web/API
- **Primary risks:** All auth classes listed above
- **Key review areas:** Login endpoints, middleware, session storage, password reset flows
- **OWASP references:** Authentication, Session_Management, CSRF_Prevention

### Android
- **Primary risks:** Biometric bypass, insecure credential storage, weak session handling
- **Key review areas:** SharedPreferences with auth tokens, biometric-only checks without backend validation
- **Extra checks:** AccountManager credential storage, OAuth redirect_uri wildcards

### iOS
- **Primary risks:** Keychain misuse, biometric bypass, weak session handling
- **Key review areas:** Keychain accessibility classes, LocalAuthentication without server token
- **Extra checks:** Universal link validation for OAuth callbacks

### Microservices
- **Primary risks:** Missing service-to-service auth, broken trust boundaries, distributed session inconsistencies
- **Key review areas:** Internal API auth, JWT validation across services, service mesh policies
- **Extra checks:** mTLS configuration, API gateway auth enforcement

## Review Instructions

### Step 1: Identify Auth Boundaries
Find all:
- Login/logout endpoints
- Permission checks (decorators, middleware, guards)
- Session creation/validation logic
- Password storage/reset flows
- OAuth/SAML handlers

### Step 2: Check Auth Enforcement
For each protected resource:
1. **Backend check present?** Don't rely on frontend hiding alone
2. **Consistent enforcement?** All paths to resource validate auth
3. **Correct subject?** Check ownership, not just "is logged in"
4. **Before operation?** Auth checked before DB query, not after

### Step 3: Review Session Security
- Cookies have `HttpOnly`, `Secure`, `SameSite=Strict/Lax`
- Session ID regenerated on privilege escalation (login, role change)
- Absolute and idle timeouts enforced
- Logout invalidates session server-side

### Step 4: Validate Password Operations
- **Storage:** bcrypt/scrypt/argon2 with salt
- **Reset:** Random tokens (128+ bits entropy), single-use, time-limited
- **Change:** Requires current password verification

### Step 5: Check CSRF Protection
- POST/PUT/DELETE require CSRF token (double-submit or synchronizer)
- `SameSite` cookie attribute set
- No state changes via GET

### Step 6: Review OAuth/SAML Flows
- `redirect_uri` allowlist validated
- PKCE used for mobile/SPA clients
- `state` parameter validated
- JWT signatures verified with correct algorithm

### Step 7: Report Findings
For each vulnerability:
- **Severity:** Critical (auth bypass, password storage), High (CSRF, session fixation)
- **Location:** File, line, endpoint
- **Description:** Specific attack vector
- **Fix:** Code-level remediation with example

## Examples

### ✅ SAFE: Permission Check Before Query
```python
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)
    db.session.delete(post)
```

### ❌ UNSAFE: Missing Ownership Check
```python
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
```
**Finding:** Critical — Authorization bypass. Any authenticated user can delete any post.

### ✅ SAFE: CSRF Protection (Django)
```python
@require_http_methods(["POST"])
@csrf_protect
def transfer_funds(request):
    # CSRF token validated automatically
    amount = request.POST['amount']
```

### ❌ UNSAFE: No CSRF Token
```python
@app.post('/transfer')
def transfer(request):
    amount = request.form['amount']
    transfer_money(amount)
```
**Finding:** High — CSRF vulnerability. Attacker can forge requests from victim's browser.

### ✅ SAFE: Password Hashing (Python)
```python
from werkzeug.security import generate_password_hash
hashed = generate_password_hash(password, method='pbkdf2:sha256')
```

### ❌ UNSAFE: Plaintext Password
```python
user.password = password
db.session.commit()
```
**Finding:** Critical — Plaintext password storage. Use bcrypt/scrypt/argon2.

## Migration Coverage

## OWASP References
- [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
- [OAuth2 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html)

## Quick Checklist
- [ ] All protected endpoints have backend auth checks
- [ ] Ownership validated, not just authentication status
- [ ] Session cookies use `HttpOnly`, `Secure`, `SameSite`
- [ ] CSRF tokens on all state-changing operations
- [ ] Passwords hashed with bcrypt/scrypt/argon2
- [ ] Password reset tokens random, single-use, time-limited
- [ ] OAuth `redirect_uri` validated against allowlist
- [ ] No hardcoded credentials in code
