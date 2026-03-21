---
name: security-mobile
description: >
  Comprehensive mobile security review covering Android MASVS (exported components, Intent injection,
  WebView, insecure storage, Keystore, network_security_config, logging, backup) and iOS MASVS
  (ATS bypass, URL scheme, Keychain, pasteboard, screenshot, CommonCrypto, jailbreak, insecure storage)
  plus shared mobile concerns (cert pinning, biometric, deep links, binary hardening, privacy).
  Trigger for ANY mobile code review (.kt, .java, .swift, .m files) or mobile platform changes.
---

# Security Review: Mobile Platform Vulnerabilities

## Purpose
Comprehensive security review for mobile applications covering OWASP MASVS controls: storage security, cryptography, authentication, network security, platform interaction, code quality, and resilience. Covers both Android and iOS platforms plus shared mobile security concerns.

## Scope
This skill covers **21 mobile security classes** organized by platform:

**Android (8):** Insecure storage, exported components, Intent injection, WebView security, insecure crypto, network security config, logging sensitive data, backup exposure

**iOS (8):** Insecure storage, ATS bypass, URL scheme hijacking, Keychain misuse, pasteboard leaks, screenshot exposure, insecure crypto, jailbreak detection bypass

**Shared (5):** Certificate pinning, biometric auth bypass, deep link hijacking, binary hardening, privacy/data collection

## Detection Strategy — Android

### 1. Android Insecure Storage `[MASVS-STORAGE]`
- **SharedPreferences in MODE_WORLD_READABLE** (deprecated but still in legacy code)
- **Plaintext secrets** in SharedPreferences without EncryptedSharedPreferences
- **SQLite databases** with sensitive data unencrypted
- **External storage** (SD card) for sensitive files
- **Hardcoded secrets** in strings.xml or BuildConfig

**Red flags:**
```kotlin
// ❌ UNSAFE
val prefs = getSharedPreferences("auth", Context.MODE_PRIVATE)
prefs.edit().putString("api_key", apiKey).apply()  // Plaintext
```

### 2. Android Exported Components `[MASVS-PLATFORM]`
- **Exported=true** without permission checks
- **Intent filters** making components implicitly exported
- **ContentProviders** exported by default (API <17)
- **Missing signature-level permissions** for inter-app communication

**Red flags:**
```xml
<!-- ❌ UNSAFE -->
<activity android:name=".AdminActivity" android:exported="true" />
<service android:name=".PaymentService" android:exported="true" />
```

### 3. Android Intent Injection `[MASVS-PLATFORM]`
- **Unvalidated Intent extras** passed to startActivity
- **Implicit Intents** for sensitive operations
- **PendingIntent** with mutable flags (FLAG_MUTABLE on API 31+)
- **Intent data** not sanitized before use

**Red flags:**
```kotlin
// ❌ UNSAFE
val url = intent.getStringExtra("url")
webView.loadUrl(url)  // Attacker-controlled URL
```

### 4. Android WebView Security `[MASVS-PLATFORM]`
- **JavaScript enabled** with untrusted content
- **File access enabled** (setAllowFileAccess)
- **Universal XSS** via loadDataWithBaseURL with file://
- **Missing WebViewClient.shouldOverrideUrlLoading** validation
- **@JavascriptInterface** exposed to untrusted pages

**Red flags:**
```kotlin
// ❌ UNSAFE
webView.settings.javaScriptEnabled = true
webView.settings.allowFileAccessFromFileURLs = true
webView.addJavascriptInterface(jsInterface, "Android")
webView.loadUrl(userProvidedUrl)
```

### 5. Android Insecure Crypto `[MASVS-CRYPTO]`
- **Hardcoded encryption keys** in code
- **Weak algorithms** (DES, RC4, MD5)
- **ECB mode** (predictable patterns)
- **Not using Android Keystore** for key storage
- **Predictable IVs** or reused IVs

**Red flags:**
```kotlin
// ❌ UNSAFE
val key = "hardcoded1234567"
val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
```

### 6. Android Network Security Config `[MASVS-NETWORK]`
- **cleartextTrafficPermitted=true**
- **Custom trust anchors** without certificate pinning
- **Debug certificates trusted** in release builds
- **Missing network_security_config.xml** (defaults to cleartext allowed on API <28)

**Red flags:**
```xml
<!-- ❌ UNSAFE -->
<network-security-config>
    <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

### 7. Android Logging Sensitive Data `[MASVS-STORAGE]`
- **Log.d/Log.i** with PII, tokens, keys in release builds
- **No ProGuard** removing logs
- **Stack traces** logged with sensitive data
- **Crashlytics/Sentry** without data sanitization

**Red flags:**
```kotlin
// ❌ UNSAFE
Log.d("Auth", "Token: $authToken")
Log.i("User", "SSN: ${user.ssn}")
```

### 8. Android Backup Exposure `[MASVS-STORAGE]`
- **allowBackup=true** without fullBackupContent rules
- **Auto-backup including sensitive files** (databases, SharedPreferences)
- **No android:fullBackupOnly**
- **Cloud backup enabled** for sensitive apps

**Red flags:**
```xml
<!-- ❌ UNSAFE -->
<application android:allowBackup="true" ... >
```

## Detection Strategy — iOS

### 1. iOS Insecure Storage `[MASVS-STORAGE]`
- **UserDefaults** for sensitive data (tokens, keys)
- **Plist files** with secrets in app bundle or Documents
- **Core Data** without encryption
- **Not using Keychain** for credentials

**Red flags:**
```swift
// ❌ UNSAFE
UserDefaults.standard.set(apiToken, forKey: "token")
try? data.write(to: documentsURL.appendingPathComponent("secret.dat"))
```

### 2. iOS ATS Bypass `[MASVS-NETWORK]`
- **NSAllowsArbitraryLoads=true** in Info.plist
- **NSExceptionDomains** disabling ATS for production domains
- **NSAllowsArbitraryLoadsInWebContent** for WKWebView
- **NSExceptionAllowsInsecureHTTPLoads** for specific domains

**Red flags:**
```xml
<!-- ❌ UNSAFE -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### 3. iOS URL Scheme Hijacking `[MASVS-PLATFORM]`
- **Custom URL schemes** without validation
- **Universal Links** misconfigured or not implemented
- **URL parameters** not sanitized before use
- **No AASA file** (Apple App Site Association) for universal links

**Red flags:**
```swift
// ❌ UNSAFE
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
    webView.load(URLRequest(url: url))  // Unvalidated
    return true
}
```

### 4. iOS Keychain Misuse `[MASVS-CRYPTO]`
- **Wrong accessibility class** (e.g., kSecAttrAccessibleAlways instead of WhenUnlocked)
- **No kSecAttrAccessControl** for Touch ID/Face ID items
- **Keychain items not marked as non-migratable** (kSecAttrSynchronizable=false)
- **No Keychain access group** for shared items

**Red flags:**
```swift
// ❌ UNSAFE
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "token",
    kSecValueData as String: token.data(using: .utf8)!,
    kSecAttrAccessible as String: kSecAttrAccessibleAlways  // Wrong!
]
```

### 5. iOS Pasteboard Leak `[MASVS-STORAGE]`
- **Sensitive data** copied to UIPasteboard.general
- **No pasteboard.setItems options** (localOnly, expirationDate)
- **Password fields** allowing copy
- **Universal clipboard** syncing sensitive data to iCloud

**Red flags:**
```swift
// ❌ UNSAFE
UIPasteboard.general.string = user.creditCardNumber
```

### 6. iOS Screenshot Exposure `[MASVS-STORAGE]`
- **No blur/overlay** when app enters background (applicationDidEnterBackground)
- **Sensitive screens** not hidden during app switcher
- **Screenshots allowed** for secure content

**Red flags:**
```swift
// ❌ Missing: No applicationDidEnterBackground implementation to hide sensitive views
```

### 7. iOS Insecure Crypto `[MASVS-CRYPTO]`
- **Deprecated CommonCrypto** instead of CryptoKit
- **ECB mode** encryption
- **Hardcoded keys/IVs**
- **Weak algorithms** (DES, RC4, MD5)

**Red flags:**
```swift
// ❌ UNSAFE
let key = "hardcoded12345"
CCCrypt(CCOperation(kCCEncrypt), CCAlgorithm(kCCAlgorithmDES), ...)
```

### 8. iOS Jailbreak Detection Bypass `[MASVS-RESILIENCE]`
- **Trivial jailbreak checks** (file existence only)
- **No runtime integrity checks**
- **String-based detection** easily bypassed by hooking
- **No anti-hooking protection**

**Red flags:**
```swift
// ❌ WEAK
func isJailbroken() -> Bool {
    return FileManager.default.fileExists(atPath: "/Applications/Cydia.app")
}
```

## Detection Strategy — Shared Mobile

### 1. Certificate Pinning `[MASVS-NETWORK]`
See also: `security-supply-chain` skill for detailed pinning guidance.

### 2. Biometric Auth Bypass `[MASVS-AUTH]`
- **Local-only biometric check** without backend token validation
- **Fallback to no auth** on biometric failure
- **Biometric used as sole factor** for sensitive operations

**Red flags (iOS):**
```swift
// ❌ UNSAFE: Local-only
let context = LAContext()
if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: nil) {
    context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Auth") { success, _ in
        if success {
            self.showSecretData()  // No backend verification!
        }
    }
}
```

### 3. Deep Link Hijacking `[MASVS-PLATFORM]`
- **Unvalidated deep link parameters** used in navigation
- **Open redirect** via deep link
- **XSS in WebView** via deep link
- **Multiple apps** claiming same deep link scheme

### 4. Binary Hardening `[MASVS-RESILIENCE]`
- **Missing ProGuard/R8** (Android release builds)
- **Debug symbols** in release (dSYM uploaded but not stripped)
- **No root/jailbreak detection**
- **No anti-tamper checks**

### 5. Privacy/Data Collection `[MASVS-PRIVACY]`
- **Excessive permissions** requested without justification
- **Location tracking** without user consent
- **Clipboard snooping** on app launch
- **Third-party SDKs** with tracking

## Review Instructions

### Step 1: Android Storage Security
```bash
# Search for insecure patterns
rg "MODE_WORLD_READABLE|getSharedPreferences.*MODE_PRIVATE|\.putString\(.*api|\.putString\(.*token"
rg "openOrCreateDatabase|SQLiteDatabase.openDatabase"
```

Check for EncryptedSharedPreferences usage:
```kotlin
// ✅ SAFE
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()
val prefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

### Step 2: Android Exported Components
```bash
# Check AndroidManifest.xml
grep -r "android:exported=\"true\"" AndroidManifest.xml
grep -r "<intent-filter>" AndroidManifest.xml  # Implicitly exported
```

### Step 3: iOS ATS Configuration
```bash
# Check Info.plist
grep -A 10 "NSAppTransportSecurity" */Info.plist
```

### Step 4: Biometric Implementation
```swift
// ✅ SAFE: Backend verification
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Auth") { success, error in
    if success {
        // Get short-lived token from backend
        self.apiClient.getBiometricToken { token in
            // Use token for sensitive operation
        }
    }
}
```

### Step 5: Deep Link Validation
```kotlin
// ✅ SAFE
val uri = intent.data
if (uri?.host != "myapp.com" || !uri.pathSegments.all { it.matches(Regex("[a-zA-Z0-9-]+")) }) {
    finish()
    return
}
```

## Related Review Tasks
- Android: `review-tasks/security/android/*.md` (8 tasks)
- iOS: `review-tasks/security/ios/*.md` (8 tasks)
- Mobile shared: `review-tasks/security/mobile/*.md` (5 tasks)

## OWASP References
- [Mobile Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)
- [Certificate Pinning](https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html)

## Quick Checklist — Android
- [ ] EncryptedSharedPreferences for sensitive data
- [ ] No exported components without permission checks
- [ ] Intent extras validated before use
- [ ] WebView JavaScript disabled or content trusted
- [ ] Android Keystore used for encryption keys
- [ ] network_security_config.xml with cert pinning
- [ ] Log statements removed in release (ProGuard)
- [ ] allowBackup=false or with fullBackupContent rules

## Quick Checklist — iOS
- [ ] Keychain used for sensitive data (not UserDefaults)
- [ ] ATS enabled (no NSAllowsArbitraryLoads)
- [ ] Universal Links for deep linking (not custom URL schemes alone)
- [ ] Keychain accessibility: WhenUnlocked or WhenUnlockedThisDeviceOnly
- [ ] Sensitive data not copied to general pasteboard
- [ ] Background blur implemented in applicationDidEnterBackground
- [ ] CryptoKit used (not CommonCrypto)
- [ ] Jailbreak detection with runtime integrity checks

## Quick Checklist — Shared
- [ ] Certificate pinning implemented
- [ ] Biometric auth validated by backend token
- [ ] Deep link parameters sanitized
- [ ] Code obfuscation enabled (ProGuard/R8, dSYM stripping)
- [ ] Minimal permissions requested
