---
name: security insecure crypto
description: >
  Migrated review-task skill for Insecure Cryptography. Use this skill whenever diffs
  may introduce security issues on all, especially in all. Actively look for: Insecure
  cryptography includes use of weak algorithms (DES, RC4, MD5), insecure modes (ECB),
  hardcoded encryption keys, insufficient key... and report findings with high severity
  expectations and actionable fixes.
---

# Insecure Cryptography

## Source Lineage
- Original review task: `review-tasks/security/insecure-crypto.md`
- Migrated skill artifact: `skills/review-task-security-insecure-crypto/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Insecure cryptography includes use of weak algorithms (DES, RC4, MD5), insecure modes (ECB), hardcoded encryption keys, insufficient key lengths, missing initialization vectors, and improper random number generation.

## Detection Heuristics
- Deprecated/weak algorithms: DES, 3DES, RC4, MD5, SHA1 for signatures
- ECB mode for block ciphers (lacks IV, pattern-leaking)
- Hardcoded encryption keys or IVs in source code
- Key lengths below minimum: RSA < 2048 bits, AES < 128 bits
- Use of insecure random: Math.random(), rand(), srand() for crypto
- Missing authenticated encryption (use GCM, CCM, or encrypt-then-MAC)

## Eval Cases
### Case 1: AES ECB mode
```python
# BUGGY CODE — should be detected
from Crypto.Cipher import AES
key = b'sixteen byte key'
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext.ljust(16))
```
**Expected finding:** High — Insecure AES ECB mode. Identical plaintext blocks produce identical ciphertext (leaks patterns, e.g., penguin image attack). Use AES-GCM or AES-CBC with random IV: `AES.new(key, AES.MODE_GCM)`.

### Case 2: Hardcoded encryption key
```javascript
// BUGGY CODE — should be detected
const crypto = require('crypto');
const SECRET_KEY = 'my-secret-key-12345678901234567890'; // 32 bytes
function encrypt(data) {
  const cipher = crypto.createCipheriv('aes-256-cbc', SECRET_KEY, iv);
  return cipher.update(data, 'utf8', 'hex') + cipher.final('hex');
}
```
**Expected finding:** Critical — Hardcoded encryption key. Key embedded in source code, visible in version control. Load keys from secure environment variables or key management service (AWS KMS, Azure Key Vault, HashiCorp Vault).

### Case 3: Weak RSA key length
```java
// BUGGY CODE — should be detected
import java.security.KeyPairGenerator;
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(1024); // Too weak
KeyPair pair = keyGen.generateKeyPair();
```
**Expected finding:** High — Weak RSA key length (1024 bits). Vulnerable to factorization attacks with modern compute. Use minimum 2048 bits (NIST recommendation), prefer 3072+ for long-term security.

## Counter-Examples
### Counter 1: AES-GCM with random IV
```python
# CORRECT CODE — should NOT be flagged
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32) # 256-bit key from secure source
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
# Store: cipher.nonce, tag, ciphertext
```
**Why it's correct:** AES-GCM with random nonce, authenticated encryption, key from secure RNG.

### Counter 2: Key from environment variable
```javascript
// CORRECT CODE — should NOT be flagged
const crypto = require('crypto');
const SECRET_KEY = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
if (SECRET_KEY.length !== 32) {
  throw new Error('Invalid key length');
}
function encrypt(data) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', SECRET_KEY, iv);
  // ...
}
```
**Why it's correct:** Key loaded from environment variable, validated length, random IV per encryption.

## Binary Eval Assertions
- [ ] Detects AES ECB mode in eval case 1
- [ ] Detects hardcoded key in eval case 2
- [ ] Detects weak RSA key length in eval case 3
- [ ] Does NOT flag counter-example 1 (AES-GCM with random IV)
- [ ] Does NOT flag counter-example 2 (key from environment)
- [ ] Finding references OWASP Cryptographic Storage Cheat Sheet
- [ ] Severity assigned as high or critical for hardcoded keys

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
