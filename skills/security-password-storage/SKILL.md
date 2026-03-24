---
name: security password storage
description: >
  Insecure Password Storage. Use this skill whenever
  diffs may introduce security issues on all, especially in all. Actively look for:
  Insecure password storage includes plaintext passwords, weak hashing algorithms (MD5,
  SHA1), missing salt, inadequate work factor for bcrypt/scrypt/Argon2,... and report
  findings with critical severity expectations and actionable fixes.
---

# Insecure Password Storage
## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `all`
- Languages: `all`

## Purpose
Insecure password storage includes plaintext passwords, weak hashing algorithms (MD5, SHA1), missing salt, inadequate work factor for bcrypt/scrypt/Argon2, and reversible encryption instead of one-way hashing.

## Detection Heuristics
- Passwords stored in plaintext or with reversible encryption
- Use of fast cryptographic hashes: MD5, SHA1, SHA256 without PBKDF2/bcrypt/scrypt/Argon2
- Missing or predictable salts in password hashing
- bcrypt work factor below 10, scrypt/Argon2 with weak parameters
- Password comparison using loose equality or custom hashing without constant-time compare

## Eval Cases
### Case 1: Plaintext password storage
```python
# BUGGY CODE — should be detected
class User(db.Model):
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
```
**Expected finding:** Critical — Plaintext password storage. Passwords stored without hashing allows full database compromise if leaked. Use bcrypt, scrypt, or Argon2 with appropriate work factors.

### Case 2: Weak hashing with SHA256
```javascript
// BUGGY CODE — should be detected
const crypto = require('crypto');
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}
```
**Expected finding:** Critical — Weak password hashing with SHA256. Fast hash vulnerable to GPU-based brute force (billions of hashes/sec). Use bcrypt with cost factor >= 10: `bcrypt.hash(password, 10)`.

### Case 3: bcrypt with low work factor
```java
// BUGGY CODE — should be detected
import org.mindrot.jbcrypt.BCrypt;
public String hashPassword(String password) {
    return BCrypt.hashpw(password, BCrypt.gensalt(4)); // work factor too low
}
```
**Expected finding:** High — bcrypt work factor too low (4). Modern GPUs can brute force this quickly. Use work factor >= 10 (2^10 = 1024 rounds). Higher for sensitive systems: 12-14.

## Counter-Examples
### Counter 1: bcrypt with strong work factor
```python
# CORRECT CODE — should NOT be flagged
import bcrypt
def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    user = User(username=username, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
```
**Why it's correct:** bcrypt with work factor 12 (4096 rounds) provides strong protection against brute force.

### Counter 2: Argon2 (recommended by OWASP)
```javascript
// CORRECT CODE — should NOT be flagged
const argon2 = require('argon2');
async function hashPassword(password) {
  return await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4
  });
}
```
**Why it's correct:** Argon2id with memory-hard parameters resists GPU/ASIC attacks.

## Binary Eval Assertions
- [ ] Detects plaintext password storage in eval case 1
- [ ] Detects weak hashing (SHA256) in eval case 2
- [ ] Detects low bcrypt work factor in eval case 3
- [ ] Does NOT flag counter-example 1 (bcrypt with work factor 12)
- [ ] Does NOT flag counter-example 2 (Argon2)
- [ ] Finding recommends bcrypt/scrypt/Argon2 with work factors
- [ ] Severity assigned as critical
