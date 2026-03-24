---
name: security android webview security
description: >
  Android WebView Security. Use this skill whenever diffs
  may introduce security issues on mobile, especially in Kotlin, Java. Actively look
  for: WebView security issues include JavaScript enabled without validation, file://
  access allowing local file disclosure, addJavascriptInterface exposing native
  methods... and report findings with high severity expectations and actionable fixes.
---

# Android WebView Security
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `mobile`
- Languages: `Kotlin, Java`

## Purpose
WebView security issues include JavaScript enabled without validation, file:// access allowing local file disclosure, addJavascriptInterface exposing native methods to XSS, and missing SSL error handling.

## Detection Heuristics
- setJavaScriptEnabled(true) with untrusted content
- setAllowFileAccess(true) or setAllowUniversalAccessFromFileURLs(true)
- addJavascriptInterface without @JavascriptInterface validation
- onReceivedSslError calling handler.proceed()
- Loading user-provided URLs without allowlist

## Eval Cases
### Case 1: JavaScript enabled with addJavascriptInterface
```kotlin
// BUGGY CODE — should be detected
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(NativeBridge(), "Android")

class NativeBridge {
    fun getSecrets(): String {
        return "API_KEY=secret123"
    }
}
```
**Expected finding:** Critical — JavaScript enabled with exposed native interface. XSS in WebView can call Android.getSecrets() to steal app data. Add @JavascriptInterface annotation and validate JS bridge usage.

### Case 2: Universal file access enabled
```kotlin
// BUGGY CODE — should be detected
webView.settings.apply {
    allowFileAccess = true
    allowFileAccessFromFileURLs = true
    allowUniversalAccessFromFileURLs = true
}
webView.loadUrl("file:///android_asset/index.html")
```
**Expected finding:** High — Universal file access from file URLs allows JavaScript to read arbitrary local files via XHR. Disable file access or use https:// with proper CSP.

## Counter-Examples
### Counter 1: Secure WebView configuration
```kotlin
// CORRECT CODE — should NOT be flagged
webView.settings.apply {
    javaScriptEnabled = false // Or true only for trusted content
    allowFileAccess = false
    allowFileAccessFromFileURLs = false
    allowUniversalAccessFromFileURLs = false
}
webView.webViewClient = object : WebViewClient() {
    override fun onReceivedSslError(view: WebView, handler: SslErrorHandler, error: SslError) {
        handler.cancel() // Don't proceed on SSL error
    }
}
```
**Why it's correct:** JavaScript disabled or used only with trusted content, file access blocked, SSL errors rejected.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes actionable fix suggestion
- [ ] Severity assigned as high
- [ ] References OWASP MASVS-PLATFORM
