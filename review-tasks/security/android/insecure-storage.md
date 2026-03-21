# Task: Android Insecure Storage

## Category
security

## Severity
high

## Platforms
mobile

## Languages
Kotlin, Java

## Description
Android insecure storage includes storing sensitive data in SharedPreferences, SQLite databases, or external storage without encryption, using world-readable file permissions, and missing Android Keystore for cryptographic keys.

## Detection Heuristics
- Sensitive data (tokens, passwords, PII) in SharedPreferences without EncryptedSharedPreferences
- SQLite databases storing plaintext secrets
- Files created with MODE_WORLD_READABLE
- Cryptographic keys hardcoded or stored in assets
- Missing Android Keystore usage for key material
- Backups enabled for app with sensitive data (allowBackup=true)

## Eval Cases

### Case 1: Plaintext SharedPreferences
```kotlin
// BUGGY CODE — should be detected
val prefs = getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
prefs.edit()
    .putString("auth_token", authToken)
    .putString("credit_card", cardNumber)
    .apply()
```
**Expected finding:** High — Sensitive data (auth token, credit card) stored in plaintext SharedPreferences. Rooted devices or ADB backup can extract. Use EncryptedSharedPreferences with Android Keystore.

### Case 2: SQLite with plaintext passwords
```java
// BUGGY CODE — should be detected
public void saveUser(String username, String password) {
    ContentValues values = new ContentValues();
    values.put("username", username);
    values.put("password", password); // Plaintext!
    db.insert("users", null, values);
}
```
**Expected finding:** Critical — Password stored in plaintext SQLite database. Use password hashing (bcrypt/Argon2) for passwords, or EncryptedSharedPreferences for tokens.

### Case 3: Hardcoded encryption key
```kotlin
// BUGGY CODE — should be detected
object CryptoUtils {
    private const val SECRET_KEY = "0123456789abcdef" // Hardcoded!
    
    fun encrypt(data: String): String {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        val keySpec = SecretKeySpec(SECRET_KEY.toByteArray(), "AES")
        cipher.init(Cipher.ENCRYPT_MODE, keySpec)
        return Base64.encodeToString(cipher.doFinal(data.toByteArray()), Base64.DEFAULT)
    }
}
```
**Expected finding:** Critical — Hardcoded encryption key. Key visible via reverse engineering (APK unzip + jadx). Use Android Keystore to generate/store keys: `KeyGenerator.getInstance("AES", "AndroidKeyStore")`.

## Counter-Examples

### Counter 1: EncryptedSharedPreferences
```kotlin
// CORRECT CODE — should NOT be flagged
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedPrefs.edit()
    .putString("auth_token", authToken)
    .apply()
```
**Why it's correct:** Uses EncryptedSharedPreferences with Android Keystore-backed master key.

### Counter 2: Android Keystore for encryption
```kotlin
// CORRECT CODE — should NOT be flagged
val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
val keyGenSpec = KeyGenParameterSpec.Builder(
    "app_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .build()
keyGenerator.init(keyGenSpec)
val secretKey = keyGenerator.generateKey()
```
**Why it's correct:** Key generated and stored in Android Keystore hardware-backed security.

## Binary Eval Assertions
- [ ] Detects plaintext SharedPreferences in eval case 1
- [ ] Detects plaintext SQLite password in eval case 2
- [ ] Detects hardcoded key in eval case 3
- [ ] Does NOT flag counter-example 1 (EncryptedSharedPreferences)
- [ ] Does NOT flag counter-example 2 (Android Keystore)
- [ ] Finding references OWASP MASVS-STORAGE
- [ ] Severity assigned as high or critical
