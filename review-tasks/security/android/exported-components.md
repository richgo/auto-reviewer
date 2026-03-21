# Task: Android Exported Components

## Category
security

## Severity
critical

## Platforms
mobile

## Languages
Kotlin, Java, XML

## Description
Exported Android components (Activities, Services, BroadcastReceivers, ContentProviders) without proper permission checks allow malicious apps to invoke them, steal data, or trigger unauthorized actions.

## Detection Heuristics
- `android:exported="true"` without permission attribute
- Intent filters on components making them implicitly exported (Android < 12)
- Activities accepting Intent extras without validation
- ContentProviders with `android:exported="true"` lacking permissions
- Broadcast receivers with no signature-level permission

## Eval Cases

### Case 1: Exported Activity without validation
```xml
<!-- AndroidManifest.xml - BUGGY CODE -->
<activity
    android:name=".AdminActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="com.example.ADMIN_ACTION" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
</activity>
```
```kotlin
// AdminActivity.kt
class AdminActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // No permission check!
        val action = intent.getStringExtra("admin_action")
        executeAdminAction(action)
    }
}
```
**Expected finding:** Critical — Exported Activity accessible by any app without permission check. Malicious app can launch admin functions. Add `android:permission="signature"` or check caller in code.

### Case 2: Exported ContentProvider
```xml
<!-- BUGGY CODE — should be detected -->
<provider
    android:name=".UserDataProvider"
    android:authorities="com.example.provider"
    android:exported="true" /> <!-- No permission! -->
```
**Expected finding:** Critical — ContentProvider exported without readPermission/writePermission. Any app can query/modify user data. Add `android:permission` or `android:readPermission`/`android:writePermission` with signature-level protection.

### Case 3: BroadcastReceiver without permission
```xml
<!-- BUGGY CODE — should be detected -->
<receiver
    android:name=".PaymentReceiver"
    android:exported="true">
    <intent-filter>
        <action android:name="com.example.PROCESS_PAYMENT" />
    </intent-filter>
</receiver>
```
**Expected finding:** High — Exported BroadcastReceiver for sensitive action without permission. Malicious app can send fake payment broadcasts. Require signature permission or use LocalBroadcastManager.

## Counter-Examples

### Counter 1: Activity with signature permission
```xml
<!-- CORRECT CODE — should NOT be flagged -->
<permission
    android:name="com.example.ADMIN_PERMISSION"
    android:protectionLevel="signature" />

<activity
    android:name=".AdminActivity"
    android:permission="com.example.ADMIN_PERMISSION"
    android:exported="true">
    <intent-filter>
        <action android:name="com.example.ADMIN_ACTION" />
    </intent-filter>
</activity>
```
**Why it's correct:** Activity protected by signature-level permission (only same-signature apps can access).

### Counter 2: Non-exported component
```xml
<!-- CORRECT CODE — should NOT be flagged -->
<receiver
    android:name=".InternalReceiver"
    android:exported="false"> <!-- Not accessible externally -->
    <intent-filter>
        <action android:name="com.example.INTERNAL_ACTION" />
    </intent-filter>
</receiver>
```
**Why it's correct:** Component explicitly not exported, only accessible within app.

## Binary Eval Assertions
- [ ] Detects exported Activity without permission in eval case 1
- [ ] Detects exported ContentProvider in eval case 2
- [ ] Detects exported BroadcastReceiver in eval case 3
- [ ] Does NOT flag counter-example 1 (signature permission)
- [ ] Does NOT flag counter-example 2 (exported=false)
- [ ] Finding references OWASP MASVS-PLATFORM
- [ ] Severity assigned as critical
