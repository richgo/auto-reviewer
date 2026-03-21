# Task: Session Management Flaws

## Category
security

## Severity
high

## Platforms
web, api

## Languages
all

## Description
Session management flaws include predictable session IDs, missing session expiration, session fixation vulnerabilities, insecure session storage, and failure to invalidate sessions on logout or password change.

## Detection Heuristics
- Predictable or sequential session ID generation
- Session cookies missing Secure, HttpOnly, or SameSite flags
- No session timeout or excessively long session lifetimes
- Sessions not invalidated on logout, password change, or privilege escalation
- Session ID exposed in URL parameters
- Accepting session ID from query string instead of only cookies

## Eval Cases

### Case 1: Session cookie missing security flags
```python
# BUGGY CODE — should be detected
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        session['user_id'] = user.id
        response = make_response(redirect('/dashboard'))
        response.set_cookie('session_id', generate_session_id())
        return response
```
**Expected finding:** High — Session cookie missing security flags. Cookie lacks Secure (HTTPS-only), HttpOnly (no JS access), and SameSite (CSRF protection) flags. Set all three: `response.set_cookie('session_id', value, secure=True, httponly=True, samesite='Strict')`.

### Case 2: No session invalidation on logout
```javascript
// BUGGY CODE — should be detected
app.post('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/login');
});
```
**Expected finding:** High — Session destroyed client-side only. Session remains valid on server if session ID is captured. Implement server-side session revocation list or database flag. Also clear cookie: `res.clearCookie('sessionId')`.

### Case 3: Session fixation vulnerability
```java
// BUGGY CODE — should be detected
public void doLogin(HttpServletRequest request, HttpServletResponse response) {
    String username = request.getParameter("username");
    HttpSession session = request.getSession(); // reuses existing session
    session.setAttribute("username", username);
    session.setAttribute("authenticated", true);
}
```
**Expected finding:** Critical — Session fixation vulnerability. Accepts pre-existing session ID from attacker. Regenerate session ID after successful authentication: `request.changeSessionId()` or `session.invalidate(); session = request.getSession(true)`.

## Counter-Examples

### Counter 1: Secure session cookie configuration
```python
# CORRECT CODE — should NOT be flagged
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
)
```
**Why it's correct:** Flask session configured with all security flags and reasonable timeout.

### Counter 2: Session regeneration on login
```java
// CORRECT CODE — should NOT be flagged
public void doLogin(HttpServletRequest request, HttpServletResponse response) {
    String username = request.getParameter("username");
    HttpSession oldSession = request.getSession(false);
    if (oldSession != null) {
        oldSession.invalidate();
    }
    HttpSession newSession = request.getSession(true);
    newSession.setAttribute("username", username);
    newSession.setAttribute("authenticated", true);
}
```
**Why it's correct:** Invalidates old session and creates new one, preventing session fixation.

## Binary Eval Assertions
- [ ] Detects missing cookie security flags in eval case 1
- [ ] Detects incomplete logout in eval case 2
- [ ] Detects session fixation in eval case 3
- [ ] Does NOT flag counter-example 1 (secure cookie config)
- [ ] Does NOT flag counter-example 2 (session regeneration)
- [ ] Finding includes fix with Secure/HttpOnly/SameSite flags
- [ ] Severity assigned as high or critical for fixation
