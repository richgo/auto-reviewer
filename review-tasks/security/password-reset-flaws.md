# Task: Password Reset Flaws

## Category
security

## Severity
high

## Platforms
web, api

## Languages
all

## Description
Password reset flaws include predictable reset tokens, token reuse, missing token expiration, lack of rate limiting, insecure delivery channels, and failure to invalidate existing sessions after reset.

## Detection Heuristics
- Predictable or sequential reset tokens (timestamp-based, auto-increment)
- Reset tokens with insufficient entropy (< 128 bits)
- Missing expiration time on reset tokens
- Tokens not invalidated after use
- Reset tokens sent via insecure channels (HTTP, email without TLS)
- No rate limiting on reset requests per email/account
- Sessions not invalidated after password change

## Eval Cases

### Case 1: Predictable reset token
```python
# BUGGY CODE — should be detected
import time
def generate_reset_token(user_id):
    return str(user_id) + str(int(time.time()))

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        token = generate_reset_token(user.id)
        user.reset_token = token
        send_email(user.email, f'Reset link: /reset/{token}')
```
**Expected finding:** Critical — Predictable password reset token. Token combines user ID + timestamp, easily brute-forced. Use cryptographically secure random tokens: `secrets.token_urlsafe(32)` (256 bits).

### Case 2: No token expiration
```javascript
// BUGGY CODE — should be detected
app.post('/reset/:token', async (req, res) => {
  const user = await User.findOne({ resetToken: req.params.token });
  if (user) {
    user.password = await bcrypt.hash(req.body.newPassword, 10);
    user.resetToken = null;
    await user.save();
    res.send('Password reset successful');
  }
});
```
**Expected finding:** High — Password reset token has no expiration. Token remains valid indefinitely, allowing attacker to use old intercepted tokens. Set expiration: 15-60 minutes max.

### Case 3: Sessions not invalidated after reset
```java
// BUGGY CODE — should be detected
@PostMapping("/reset-password")
public ResponseEntity resetPassword(@RequestParam String token, @RequestParam String newPassword) {
    PasswordResetToken resetToken = tokenRepository.findByToken(token);
    if (resetToken != null && !resetToken.isExpired()) {
        User user = resetToken.getUser();
        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        tokenRepository.delete(resetToken);
        return ResponseEntity.ok("Password reset successful");
    }
    return ResponseEntity.badRequest().build();
}
```
**Expected finding:** High — Existing sessions not invalidated after password reset. Attacker who gained session access can continue using account even after victim resets password. Invalidate all active sessions when password changes.

## Counter-Examples

### Counter 1: Secure reset token with expiration
```python
# CORRECT CODE — should NOT be flagged
import secrets
from datetime import datetime, timedelta

def generate_reset_token(user):
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.now() + timedelta(minutes=30)
    db.session.commit()
    return token

@app.route('/reset/:token', methods=['POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if user and user.reset_token_expires > datetime.now():
        user.password_hash = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
        user.reset_token = None
        user.reset_token_expires = None
        # Invalidate all sessions
        Session.query.filter_by(user_id=user.id).delete()
        db.session.commit()
```
**Why it's correct:** Cryptographically secure token (256-bit), 30-minute expiration, single-use, sessions invalidated.

## Binary Eval Assertions
- [ ] Detects predictable reset token in eval case 1
- [ ] Detects missing token expiration in eval case 2
- [ ] Detects missing session invalidation in eval case 3
- [ ] Does NOT flag counter-example 1 (secure token with expiration)
- [ ] Finding recommends secrets.token_urlsafe or equivalent
- [ ] Severity assigned as high or critical for predictable tokens
- [ ] References OWASP Forgot Password Cheat Sheet
