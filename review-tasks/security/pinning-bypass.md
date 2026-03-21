# Task: Certificate Pinning Bypass

## Category
security

## Severity
high

## Platforms
mobile

## Languages
Java, Kotlin, Swift, Objective-C

## Description
Certificate pinning bypass occurs when mobile apps fail to implement or improperly implement TLS certificate pinning, allowing man-in-the-middle attacks via custom CA certificates or tools like Charles Proxy, Burp Suite, or Frida.

## Detection Heuristics
- No certificate pinning for sensitive API endpoints
- Trusting all certificates in debug/release builds
- Weak pinning implementation (easily bypassed with root/jailbreak)
- Pinning only certificate instead of public key (fragile to cert rotation)
- Missing backup pins for certificate rotation
- No SSL Pinning library used (TrustKit, OkHttp CertificatePinner)

## Eval Cases

### Case 1: Android - No certificate pinning
```kotlin
// BUGGY CODE — should be detected
val client = OkHttpClient.Builder()
    .build()

val request = Request.Builder()
    .url("https://api.bank.com/transfer")
    .build()
```
**Expected finding:** High — No certificate pinning on sensitive API. App accepts any valid certificate signed by system CAs. Attacker with custom CA can intercept traffic. Use OkHttp CertificatePinner with public key hashes.

### Case 2: iOS - Trust all certificates
```swift
// BUGGY CODE — should be detected
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    // Dangerous: accepting all certificates!
    completionHandler(.useCredential, URLCredential(trust: challenge.protectionSpace.serverTrust!))
}
```
**Expected finding:** Critical — URLSession delegate trusts all certificates. Disables all TLS validation, allows any MitM. Implement proper certificate pinning with TrustKit or check specific public keys.

### Case 3: Android - Weak pinning (certificate instead of public key)
```java
// BUGGY CODE — should be detected
CertificatePinner certificatePinner = new CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAA...") // Certificate hash, not public key
    .build();
```
**Expected finding:** Medium — Pinning certificate hash instead of public key hash. Fragile to certificate rotation, requires app update when cert renews. Pin public key (SPKI) instead: extract with `openssl x509 -pubkey`.

## Counter-Examples

### Counter 1: OkHttp with public key pinning
```kotlin
// CORRECT CODE — should NOT be flagged
val certificatePinner = CertificatePinner.Builder()
    .add("api.bank.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=") // Primary pin
    .add("api.bank.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // Backup pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```
**Why it's correct:** Public key pinning with primary + backup pins for rotation.

### Counter 2: iOS with TrustKit
```swift
// CORRECT CODE — should NOT be flagged
import TrustKit

let trustKitConfig: [String: Any] = [
    kTSKSwizzleNetworkDelegates: false,
    kTSKPinnedDomains: [
        "api.example.com": [
            kTSKPublicKeyHashes: [
                "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
            ],
            kTSKEnforcePinning: true
        ]
    ]
]

TrustKit.initSharedInstance(withConfiguration: trustKitConfig)
```
**Why it's correct:** TrustKit enforces public key pinning with backup pins.

## Binary Eval Assertions
- [ ] Detects missing pinning in eval case 1
- [ ] Detects trust-all bypass in eval case 2
- [ ] Detects certificate hash pinning in eval case 3
- [ ] Does NOT flag counter-example 1 (OkHttp public key pinning)
- [ ] Does NOT flag counter-example 2 (TrustKit)
- [ ] Finding recommends public key pinning with backup pins
- [ ] Severity assigned as high for sensitive endpoints
