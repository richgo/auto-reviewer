---
name: security-data-protection
description: >
  Detect data protection vulnerabilities: secrets exposure in logs/code/repos, path traversal,
  mass assignment, insecure cryptography, insecure deserialization, and file upload bypasses.
  Trigger when reviewing file operations, crypto usage, logging, serialization, or any code
  handling sensitive data or user-uploaded files.
---

# Security Review: Data Protection

## Purpose
Review code for vulnerabilities that expose or compromise sensitive data through insecure storage, weak encryption, unsafe deserialization, file operations, or overly permissive data binding.

## Scope
Six data protection vulnerability classes:
1. **Secrets Exposure** — API keys, tokens, passwords in code, logs, or repos
2. **Path Traversal** — file operations with unsanitized paths
3. **Mass Assignment** — over-binding parameters to models
4. **Insecure Crypto** — weak algorithms, hardcoded keys, ECB mode
5. **Insecure Deserialization** — unsafe unpickling/unmarshalling
6. **File Upload** — insufficient validation, execution of uploaded files

## Detection Strategy

### Universal Red Flags
- **Hardcoded secrets** (API keys, passwords, tokens) in code
- **Logging sensitive data** (passwords, tokens, PII)
- **User-controlled file paths** without canonicalization
- **ECB mode** in encryption
- **Deserialization of untrusted data** (pickle, YAML, XML)
- **File uploads without type validation** or size limits

### High-Risk Patterns

**Secrets Exposure:**
- `API_KEY = "sk-abc123..."`
- `password = "admin123"`
- `logger.info(f"Token: {token}")`
- Secrets in `.env` committed to git
- AWS keys in config files

**Path Traversal:**
- `open(f"uploads/{filename}")`
- `File(userPath)`
- `fs.readFile(req.query.file)`
- No path canonicalization or allowlist check

**Mass Assignment:**
- `user.update(request.POST)`
- `User.create(req.body)`
- No field allowlist (e.g., `permit(:name, :email)`)

**Insecure Crypto:**
- `DES`, `RC4`, `MD5`, `SHA1` for security purposes
- `AES/ECB` mode (no IV)
- Hardcoded encryption keys
- Custom crypto implementations

**Insecure Deserialization:**
- `pickle.loads(user_data)`
- `yaml.load()` instead of `yaml.safe_load()`
- `unserialize()` on user input (PHP)
- `ObjectInputStream.readObject()` without validation

**File Upload:**
- No MIME type validation
- Trusting client-provided `Content-Type`
- Executable file extensions not blocked
- No virus scanning
- Files served from upload directory without sandboxing

## Platform-Specific Guidance

### Web/API
- **Primary risks:** All data protection classes listed
- **Key review areas:** File upload handlers, crypto libraries, ORM mass assignment, logging middleware
- **OWASP references:** Secrets_Management, Cryptographic_Storage, File_Upload

### Android
- **Primary risks:** Secrets in SharedPreferences/code, insecure crypto, logging PII
- **Key review areas:** `SharedPreferences`, `Log.d/i`, hardcoded keys, `EncryptedSharedPreferences` misuse
- **Extra checks:** World-readable files, missing Keystore usage

### iOS
- **Primary risks:** Secrets in UserDefaults/code, insecure crypto, Keychain misuse
- **Key review areas:** `UserDefaults`, hardcoded secrets, CommonCrypto usage, ECB mode
- **Extra checks:** Keychain accessibility class (`kSecAttrAccessibleAfterFirstUnlock` too permissive)

### Microservices
- **Primary risks:** Secrets in environment variables, config stored in repos, insecure inter-service encryption
- **Key review areas:** Kubernetes secrets management, service mesh mTLS, secret injection
- **Extra checks:** Secrets in Docker image layers, unencrypted service-to-service comms

## Review Instructions

### Step 1: Hunt for Secrets
Search for:
- String literals matching API key patterns (`sk-`, `AIza`, `ghp_`, etc.)
- Variable names: `password`, `secret`, `api_key`, `token`, `private_key`
- Config files committed to git (`.env`, `secrets.yml`, `config.json`)
- Logs containing sensitive data

### Step 2: Check File Operations
For `open()`, `readFile()`, `File()`, etc.:
1. **Source:** Is path user-controlled?
2. **Validation:** Canonicalize path, check prefix against allowlist
3. **Traversal check:** Reject `..`, absolute paths, symlinks

### Step 3: Review Crypto Usage
- **Algorithm:** AES-GCM, ChaCha20-Poly1305, or AES-CBC with HMAC (NOT DES, RC4, ECB)
- **Key management:** Keys from secure storage (Keychain, Keystore, KMS), not hardcoded
- **IV/Nonce:** Randomly generated per encryption, not reused
- **Libraries:** Use platform crypto (CommonCrypto, javax.crypto, Web Crypto API), not custom

### Step 4: Validate Deserialization
- **Never deserialize untrusted data** with unsafe formats (pickle, YAML, Java serialization)
- Use safe alternatives: JSON, protobuf, MessagePack
- If deserialization necessary: validate structure, use allowlists, sandbox execution

### Step 5: Review File Uploads
- **Validation:** Allowlist MIME types, check magic bytes (not just extension)
- **Storage:** Outside webroot, randomize filenames, separate storage service (S3)
- **Execution prevention:** Set `X-Content-Type-Options: nosniff`, serve with `Content-Disposition: attachment`
- **Size limits:** Enforce max upload size

### Step 6: Check Mass Assignment
- **Allowlist fields:** Use strong parameters (Rails), DTOs (Java), field selection (Django)
- **Deny by default:** Never bind all request data to model
- **Protect sensitive fields:** `is_admin`, `role`, `balance`

### Step 7: Report Findings
For each vulnerability:
- **Severity:** Critical (secrets in code/logs, path traversal, insecure deserialization), High (weak crypto, file upload bypass, mass assignment)
- **Location:** File, line
- **Description:** Specific exposure or attack vector
- **Fix:** Remediation with code example

## Examples

### ✅ SAFE: Secret from Environment
```python
import os
api_key = os.environ['API_KEY']
```

### ❌ UNSAFE: Hardcoded Secret
```python
api_key = "sk-abc123456789"
```
**Finding:** Critical — API key hardcoded in source. Move to environment variable or secrets manager.

### ✅ SAFE: Path Canonicalization
```python
import os
base = "/var/uploads"
filename = secure_filename(request.files['file'].filename)
path = os.path.join(base, filename)
if not os.path.realpath(path).startswith(base):
    abort(400)
```

### ❌ UNSAFE: Path Traversal
```python
filename = request.args.get('file')
with open(f"/var/uploads/{filename}") as f:
    return f.read()
```
**Finding:** Critical — Path traversal. Attacker can read arbitrary files with `../../etc/passwd`.

### ✅ SAFE: AES-GCM Encryption
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
nonce = os.urandom(12)
ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
```

### ❌ UNSAFE: ECB Mode
```python
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(plaintext))
```
**Finding:** High — AES-ECB mode leaks patterns. Use AES-GCM or AES-CBC with HMAC.

### ✅ SAFE: Strong Parameters (Rails)
```ruby
def user_params
  params.require(:user).permit(:name, :email)
end
```

### ❌ UNSAFE: Mass Assignment
```ruby
@user.update(params[:user])
```
**Finding:** High — Mass assignment allows setting `is_admin`, `role`. Use strong parameters.

### ✅ SAFE: Safe Deserialization
```python
import json
data = json.loads(user_input)
```

### ❌ UNSAFE: Pickle Deserialization
```python
import pickle
data = pickle.loads(user_input)
```
**Finding:** Critical — Insecure deserialization. Pickle can execute arbitrary code. Use JSON.

## Migration Coverage
Review guidance from the legacy review-task corpus is now consolidated in this skill and validated via the migration inventory (`openspec/changes/research-changes/artifacts/review-task-skill-map.csv`).

## OWASP References
- [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Key Management](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html)
- [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [Deserialization](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [Mass Assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)

## Quick Checklist
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] File paths canonicalized and validated against allowlist
- [ ] No AES-ECB, DES, RC4, MD5 for encryption
- [ ] Encryption keys from secure storage (not hardcoded)
- [ ] No pickle/YAML/Java deserialization of untrusted data
- [ ] File uploads validated (MIME, size, magic bytes)
- [ ] Mass assignment uses field allowlists
- [ ] Sensitive data not logged (passwords, tokens, PII)
