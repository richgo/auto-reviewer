# Task: Authentication Flaws

## Category
security

## Severity
critical

## Platforms
all

## Languages
all

## Description
Authentication flaws include weak password policies, missing multi-factor authentication, insecure password reset mechanisms, lack of account lockout, and credential exposure during transmission or storage.

## Detection Heuristics
- Missing password complexity requirements or minimum length checks
- No rate limiting or account lockout after failed login attempts
- Credentials transmitted over unencrypted connections
- Authentication state stored in client-side cookies without signatures
- Missing multi-factor authentication for sensitive operations
- Weak security questions or recoverable password hints

## Eval Cases

### Case 1: No account lockout after failed attempts
```python
# BUGGY CODE — should be detected
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return redirect('/dashboard')
    return 'Invalid credentials', 401
```
**Expected finding:** Critical — Missing account lockout mechanism. No rate limiting or failed attempt tracking allows unlimited brute-force attacks. Implement account lockout after N failed attempts and exponential backoff.

### Case 2: Weak password policy
```javascript
// BUGGY CODE — should be detected
function validatePassword(password) {
  return password.length >= 6;
}
```
**Expected finding:** High — Weak password policy. Only checks minimum length (6 chars). Missing complexity requirements (uppercase, lowercase, numbers, symbols). Enforce NIST 800-63B guidelines: min 8 chars, check against breached password lists.

### Case 3: Authentication without MFA for sensitive ops
```java
// BUGGY CODE — should be detected
@PostMapping("/transfer")
public ResponseEntity transferFunds(@RequestParam String amount, @RequestParam String to) {
    if (session.getAttribute("userId") == null) {
        return ResponseEntity.status(401).build();
    }
    // No MFA check before money transfer
    bankService.transfer(session.getAttribute("userId"), to, amount);
    return ResponseEntity.ok().build();
}
```
**Expected finding:** Critical — Missing MFA for sensitive operation. Financial transfer requires only session cookie. Add second factor verification (TOTP, SMS, biometric) for high-risk actions.

## Counter-Examples

### Counter 1: Account lockout with exponential backoff
```python
# CORRECT CODE — should NOT be flagged
from datetime import datetime, timedelta
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.locked_until and user.locked_until > datetime.now():
            return 'Account locked', 429
        if user.check_password(password):
            user.failed_attempts = 0
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.locked_until = datetime.now() + timedelta(minutes=15)
            db.session.commit()
    return 'Invalid credentials', 401
```
**Why it's correct:** Implements account lockout after 5 failed attempts with 15-minute cooldown.

### Counter 2: Strong password validation
```javascript
// CORRECT CODE — should NOT be flagged
const zxcvbn = require('zxcvbn');
function validatePassword(password) {
  const result = zxcvbn(password);
  return password.length >= 12 && result.score >= 3;
}
```
**Why it's correct:** Uses zxcvbn for entropy checking, enforces 12+ chars and high strength score.

## Binary Eval Assertions
- [ ] Detects missing account lockout in eval case 1
- [ ] Detects weak password policy in eval case 2
- [ ] Detects missing MFA in eval case 3
- [ ] Does NOT flag counter-example 1 (account lockout implemented)
- [ ] Does NOT flag counter-example 2 (strong password validation)
- [ ] Finding references OWASP Authentication Cheat Sheet
- [ ] Severity assigned as critical for missing lockout/MFA
