# Task: Android Intent Injection

## Category
security

## Severity
high

## Platforms
mobile

## Languages
Kotlin, Java

## Description
Intent injection occurs when apps process untrusted Intent extras without validation or use implicit Intents for sensitive operations, allowing malicious apps to inject data or intercept communications.

## Detection Heuristics
- Reading Intent extras without type/null validation
- Implicit Intents for sensitive operations (file access, payments)
- Accepting file:// URIs from external Intents
- Missing Intent.setPackage() for targeted communication
- startActivity/sendBroadcast with Intents from untrusted sources

## Eval Cases

### Case 1: Unvalidated Intent extra
```kotlin
// BUGGY CODE — should be detected
class FileViewerActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val filePath = intent.getStringExtra("file_path") // No validation!
        val file = File(filePath)
        displayFile(file)
    }
}
```
**Expected finding:** High — Intent extra used without validation. Attacker can provide `../../sensitive_file` for path traversal. Validate file paths against allowlist or use Content URIs.

### Case 2: Implicit Intent for sensitive action
```kotlin
// BUGGY CODE — should be detected
fun shareConfidentialData(data: String) {
    val intent = Intent(Intent.ACTION_SEND)
    intent.putExtra(Intent.EXTRA_TEXT, data)
    intent.type = "text/plain"
    startActivity(intent) // Any app can receive!
}
```
**Expected finding:** High — Implicit Intent shares confidential data with any app via chooser. Use explicit Intent with setPackage() for known recipient or verify receiver signature.

## Counter-Examples

### Counter 1: Validated Intent with allowlist
```kotlin
// CORRECT CODE — should NOT be flagged
class FileViewerActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val filePath = intent.getStringExtra("file_path") ?: return
        val allowedDir = File(filesDir, "safe")
        val file = File(allowedDir, filePath).canonicalFile
        if (!file.startsWith(allowedDir)) {
            finish()
            return
        }
        displayFile(file)
    }
}
```
**Why it's correct:** Intent extra validated, canonical path checked against allowed directory (prevents path traversal).

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable fix suggestion
- [ ] Severity assigned as high
- [ ] References OWASP MASVS-PLATFORM
