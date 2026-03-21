---
name: security-supply-chain
description: >
  Detect supply chain security vulnerabilities: dependency vulnerabilities, certificate pinning
  bypass, and XXE (XML External Entity) attacks. Trigger when reviewing dependency updates,
  package.json/requirements.txt changes, XML parsing code, mobile network security config, or
  any code handling third-party dependencies and XML processing.
---

# Security Review: Supply Chain Vulnerabilities

## Purpose
Review code for supply chain security issues: vulnerable dependencies, missing or bypassable certificate pinning in mobile apps, and XML External Entity (XXE) injection attacks.

## Scope
This skill covers three supply chain security classes:
1. **Dependency Vulnerabilities** — outdated packages with known CVEs, typosquatting, malicious packages
2. **Certificate Pinning Bypass** — missing or improperly implemented cert pinning in mobile apps
3. **XXE (XML External Entity)** — XML parsers configured to resolve external entities

## Detection Strategy

### 1. Dependency Vulnerability Red Flags
- **Outdated packages** with known CVEs (check npm audit, pip-audit, safety)
- **Wildcard version ranges** (`*`, `latest`, `^1.x`)
- **Direct dependencies** without lock files (package-lock.json, Pipfile.lock, Gemfile.lock)
- **Installing from git repos** instead of registries
- **Missing SBOM** (Software Bill of Materials)
- **No dependency scanning** in CI/CD

**High-risk patterns:**
```json
// ❌ UNSAFE: Wildcard versions
{
  "dependencies": {
    "lodash": "*",
    "express": "^4.0.0"
  }
}
```

### 2. Certificate Pinning Bypass Red Flags
- **Missing pinning implementation** (iOS/Android network config)
- **Pinning disabled in debug builds** (and debug flag bypassable)
- **Trust all certificates** in custom TrustManager/NSURLSessionDelegate
- **Pinning only leaf certificate** (not intermediate/public key)
- **No backup pins** (rotation impossible)

**High-risk patterns (Android):**
```xml
<!-- ❌ UNSAFE: No pinning -->
<network-security-config>
    <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

**High-risk patterns (iOS):**
```swift
// ❌ UNSAFE: Trust all certificates
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    completionHandler(.useCredential, URLCredential(trust: challenge.protectionSpace.serverTrust!))
}
```

### 3. XXE Red Flags
- **XML parser with external entities enabled** (default in many parsers)
- **No DTD validation disabled**
- **Parsing untrusted XML** (user uploads, external APIs)
- **Legacy XML libraries** (pre-2015 versions)

**High-risk patterns:**
```java
// ❌ UNSAFE: XXE vulnerable
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(userUploadedFile);
```

```python
# ❌ UNSAFE: XXE vulnerable
import xml.etree.ElementTree as ET
tree = ET.parse(user_file)
```

## Platform-Specific Guidance

### Android
- **Primary risks:** Vulnerable dependencies (Gradle), missing cert pinning, insecure network_security_config
- **Key review areas:** build.gradle dependencies, network_security_config.xml, OkHttp CertificatePinner
- **OWASP references:** Mobile_Application_Security (MASVS-NETWORK), Pinning, Dependency_Check

### iOS
- **Primary risks:** Vulnerable CocoaPods/SPM deps, ATS bypass, missing cert pinning
- **Key review areas:** Podfile, Package.swift, Info.plist (NSAppTransportSecurity), URLSession delegate
- **OWASP references:** Mobile_Application_Security (MASVS-NETWORK), Pinning

### Web/API
- **Primary risks:** npm/pip vulnerabilities, XXE in API endpoints, SSRF via XXE
- **Key review areas:** package.json, XML parsing middleware, SOAP endpoints
- **OWASP references:** XXE_Prevention, Dependency_Check, npm_Security

## Review Instructions

### Step 1: Audit Dependencies

**Check for known vulnerabilities:**
```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Java
mvn dependency-check:check

# Ruby
bundle audit
```

**Check version pinning:**
```json
// ❌ UNSAFE: Unpinned
{
  "dependencies": {
    "axios": "^1.0.0",  // Could install 1.9.9 with vulnerabilities
    "lodash": "*"
  }
}

// ✅ SAFE: Pinned with lock file
{
  "dependencies": {
    "axios": "1.6.0"
  }
}
// + package-lock.json present
```

**Check for lock files:**
- **Node.js:** package-lock.json or yarn.lock
- **Python:** Pipfile.lock or poetry.lock
- **Ruby:** Gemfile.lock
- **Java:** Maven dependency:tree output committed

### Step 2: Audit Certificate Pinning (Mobile)

**Android - Check network_security_config.xml:**
```xml
<!-- ✅ SAFE: Pinning configured -->
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2025-12-31">
            <pin digest="SHA-256">base64==</pin>
            <pin digest="SHA-256">backup-pin==</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

**Android - Check OkHttp:**
```kotlin
// ✅ SAFE: OkHttp pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

**iOS - Check URLSession delegate:**
```swift
// ✅ SAFE: Public key pinning
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    guard let serverTrust = challenge.protectionSpace.serverTrust,
          let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0) else {
        completionHandler(.cancelAuthenticationChallenge, nil)
        return
    }
    
    let serverPublicKey = SecCertificateCopyKey(certificate)
    let pinnedKeys: [SecKey] = loadPinnedKeys()
    
    if pinnedKeys.contains(where: { $0 == serverPublicKey }) {
        completionHandler(.useCredential, URLCredential(trust: serverTrust))
    } else {
        completionHandler(.cancelAuthenticationChallenge, nil)
    }
}
```

### Step 3: Audit XXE Protection

**Check XML parser configuration:**

**Java:**
```java
// ✅ SAFE: XXE disabled
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
```

**Python:**
```python
# ✅ SAFE: defusedxml
from defusedxml.ElementTree import parse
tree = parse(user_file)

# ❌ UNSAFE: Standard library
import xml.etree.ElementTree as ET
tree = ET.parse(user_file)
```

**Node.js:**
```javascript
// ✅ SAFE: xml2js with XXE prevention
const xml2js = require('xml2js');
const parser = new xml2js.Parser({
  explicitCharkey: false,
  trim: false,
  normalize: false,
  normalizeTags: false,
  attrkey: '@',
  charkey: '#',
  explicitArray: false,
  ignoreAttrs: false,
  mergeAttrs: false,
  explicitRoot: false,
  validator: null,
  xmlns: false,
  explicitChildren: false,
  childkey: '$$',
  charkey: '_',
  attrNameProcessors: null,
  attrValueProcessors: null,
  tagNameProcessors: null,
  valueProcessors: null,
  emptyTag: null,
  strict: true,
  xmlns: false,
  resolveUri: false  // Prevent XXE
});
```

## Examples

### ✅ SAFE: Pinned Dependencies with Audit
```json
{
  "dependencies": {
    "express": "4.18.2",
    "lodash": "4.17.21"
  },
  "scripts": {
    "preinstall": "npm audit --audit-level=high"
  }
}
```
**With:** package-lock.json committed, CI runs `npm audit` before deploy.

### ❌ UNSAFE: Wildcard Dependencies
```json
{
  "dependencies": {
    "express": "*",
    "lodash": "^4.0.0"
  }
}
```
**Finding:** High — Wildcard versions without lock file. Vulnerable versions could be installed.

### ✅ SAFE: Android Certificate Pinning
```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.production.com", "sha256/PrimaryPin==")
    .add("api.production.com", "sha256/BackupPin==")
    .build()
```

### ❌ UNSAFE: Trust All Certificates
```kotlin
val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
    override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
})
```
**Finding:** Critical — Custom TrustManager trusts all certificates. MitM attacks possible.

### ✅ SAFE: XXE Protection (Python)
```python
from defusedxml.ElementTree import parse
tree = parse(uploaded_file)
```

### ❌ UNSAFE: XXE Vulnerable
```python
import xml.etree.ElementTree as ET
tree = ET.parse(uploaded_file)
```
**Finding:** High — XXE vulnerability. Attacker can read local files via external entity injection.

## Related Review Tasks
Detailed detection guidance for each supply chain vulnerability class:
- `review-tasks/security/dependency-vulnerability.md`
- `review-tasks/security/pinning-bypass.md`
- `review-tasks/security/xml-external-entity.md`
- `review-tasks/security/mobile/cert-pinning.md`

## OWASP References
- [Software Supply Chain Security](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- [Dependency Check](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
- [npm Security](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)
- [Certificate Pinning](https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html)
- [XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

## Quick Checklist
- [ ] All dependencies pinned with lock files committed
- [ ] npm audit / pip-audit runs in CI/CD
- [ ] No wildcard version ranges in production
- [ ] Certificate pinning implemented (mobile apps)
- [ ] Backup pins configured for rotation
- [ ] XML parsers have external entities disabled
- [ ] Using defusedxml (Python) or equivalent safe parser
- [ ] SBOM generated and reviewed
- [ ] Dependency scanning alerts monitored
