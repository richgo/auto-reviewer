---
name: review-task-security-credential-stuffing
description: >
  Migrated review-task skill for Credential Stuffing Prevention. Use this skill whenever
  diffs may introduce security issues on web, api, especially in all. Actively look for:
  Credential stuffing attacks use stolen username/password pairs from other breaches to
  compromise accounts. Prevention requires rate limiting, CAPTCHA,... and report
  findings with high severity expectations and actionable fixes.
---

# Credential Stuffing Prevention

## Source Lineage
- Original review task: `review-tasks/security/credential-stuffing.md`
- Migrated skill artifact: `skills/review-task-security-credential-stuffing/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Credential stuffing attacks use stolen username/password pairs from other breaches to compromise accounts. Prevention requires rate limiting, CAPTCHA, device fingerprinting, breach detection, and monitoring for anomalous login patterns.

## Detection Heuristics
- Missing rate limiting on authentication endpoints
- No CAPTCHA or challenge-response after repeated failures
- Lack of device fingerprinting or IP reputation checking
- No monitoring for concurrent logins from different geolocations
- Missing integration with breach notification services (HaveIBeenPwned)
- Accepting weak or commonly breached passwords

## Eval Cases
### Case 1: No rate limiting on login endpoint
```python
# BUGGY CODE — should be detected
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.authenticate(data['username'], data['password'])
    if user:
        return jsonify({'token': user.generate_token()})
    return jsonify({'error': 'Invalid credentials'}), 401
```
**Expected finding:** High — No rate limiting on authentication endpoint. Allows unlimited login attempts enabling credential stuffing attacks. Implement rate limiting: max 5 attempts per IP per minute, exponential backoff per account.

### Case 2: Missing breach password detection
```javascript
// BUGGY CODE — should be detected
async function registerUser(email, password) {
  const hashedPassword = await bcrypt.hash(password, 10);
  await db.users.insert({ email, password: hashedPassword });
  return { success: true };
}
```
**Expected finding:** Medium — Missing breach password detection. New passwords not checked against known breached password lists. Integrate HaveIBeenPwned Passwords API (k-anonymity model) or Troy Hunt's pwned-passwords library.

### Case 3: No anomaly detection for suspicious logins
```java
// BUGGY CODE — should be detected
@PostMapping("/login")
public ResponseEntity login(@RequestBody LoginRequest req, HttpServletRequest request) {
    User user = userService.authenticate(req.getUsername(), req.getPassword());
    if (user != null) {
        String token = jwtService.generateToken(user);
        return ResponseEntity.ok(new LoginResponse(token));
    }
    return ResponseEntity.status(401).build();
}
```
**Expected finding:** High — No anomaly detection on successful login. Missing checks for: new device, unusual geolocation, impossible travel, or concurrent sessions. Add device fingerprinting and alert user on suspicious activity.

## Counter-Examples
### Counter 1: Rate limiting with Flask-Limiter
```python
# CORRECT CODE — should NOT be flagged
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def api_login():
    data = request.get_json()
    user = User.authenticate(data['username'], data['password'])
    if user:
        return jsonify({'token': user.generate_token()})
    return jsonify({'error': 'Invalid credentials'}), 401
```
**Why it's correct:** Rate limiting applied to login endpoint (5 attempts/minute per IP).

### Counter 2: Breach password check with pwnedpasswords
```javascript
// CORRECT CODE — should NOT be flagged
const pwnedpasswords = require('pwnedpasswords');

async function registerUser(email, password) {
  const breachCount = await pwnedpasswords.checkPassword(password);
  if (breachCount > 0) {
    throw new Error('Password found in breach database. Choose a different password.');
  }
  const hashedPassword = await bcrypt.hash(password, 10);
  await db.users.insert({ email, password: hashedPassword });
  return { success: true };
}
```
**Why it's correct:** Checks password against HaveIBeenPwned before accepting registration.

## Binary Eval Assertions
- [ ] Detects missing rate limiting in eval case 1
- [ ] Detects missing breach detection in eval case 2
- [ ] Detects missing anomaly detection in eval case 3
- [ ] Does NOT flag counter-example 1 (rate limiting implemented)
- [ ] Does NOT flag counter-example 2 (breach password check)
- [ ] Finding references OWASP Credential Stuffing Prevention
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
