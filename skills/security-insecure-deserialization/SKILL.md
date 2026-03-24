---
name: security insecure deserialization
description: >
  Insecure Deserialization. Use this skill whenever diffs
  may introduce security issues on all, especially in Java, Python, PHP, .NET,
  JavaScript. Actively look for: Insecure deserialization occurs when untrusted data is
  deserialized without validation, allowing attackers to execute arbitrary code, perform
  object... and report findings with critical severity expectations and actionable
  fixes.
---

# Insecure Deserialization
## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `all`
- Languages: `Java, Python, PHP, .NET, JavaScript`

## Purpose
Insecure deserialization occurs when untrusted data is deserialized without validation, allowing attackers to execute arbitrary code, perform object injection, or manipulate application state through crafted serialized payloads.

## Detection Heuristics
- Deserializing untrusted user input: pickle (Python), ObjectInputStream (Java), unserialize (PHP)
- Missing type/class allowlist validation before deserialization
- Accepting serialized data from cookies, query parameters, or request bodies
- Use of insecure formats: Java native serialization, Python pickle, PHP serialize
- No integrity checks (HMAC/signature) on serialized data

## Eval Cases
### Case 1: Python pickle from user input
```python
# BUGGY CODE — should be detected
import pickle
@app.route('/load', methods=['POST'])
def load_data():
    serialized = request.data
    obj = pickle.loads(serialized) # DANGEROUS!
    return jsonify(obj)
```
**Expected finding:** Critical — Insecure deserialization with pickle. Pickle can execute arbitrary code during deserialization. Attacker can craft payload for RCE. Use JSON or msgpack for data, or sign pickled data with HMAC if necessary.

### Case 2: Java ObjectInputStream without validation
```java
// BUGGY CODE — should be detected
public Object deserialize(byte[] data) throws IOException, ClassNotFoundException {
    ByteArrayInputStream bis = new ByteArrayInputStream(data);
    ObjectInputStream ois = new ObjectInputStream(bis);
    return ois.readObject(); // No class validation!
}
```
**Expected finding:** Critical — Insecure Java deserialization. readObject() without class allowlist enables gadget chain attacks (Apache Commons Collections RCE). Implement ObjectInputFilter or avoid Java serialization entirely (use JSON/protobuf).

### Case 3: PHP unserialize from cookie
```php
// BUGGY CODE — should be detected
<?php
$user_data = unserialize($_COOKIE['user_session']);
echo "Welcome, " . $user_data['username'];
?>
```
**Expected finding:** Critical — PHP unserialize on user-controlled cookie. Enables object injection and magic method exploitation (__wakeup, __destruct) for RCE. Use JSON or signed/encrypted sessions instead.

## Counter-Examples
### Counter 1: JSON instead of pickle
```python
# CORRECT CODE — should NOT be flagged
import json
@app.route('/load', methods=['POST'])
def load_data():
    serialized = request.data
    obj = json.loads(serialized)
    return jsonify(obj)
```
**Why it's correct:** JSON cannot execute code during parsing, safe for untrusted input.

### Counter 2: Java ObjectInputFilter allowlist
```java
// CORRECT CODE — should NOT be flagged
public Object deserialize(byte[] data) throws IOException, ClassNotFoundException {
    ByteArrayInputStream bis = new ByteArrayInputStream(data);
    ObjectInputStream ois = new ObjectInputStream(bis);
    ois.setObjectInputFilter(filterInfo -> {
        if (filterInfo.serialClass() != null) {
            return filterInfo.serialClass().getName().equals("com.example.SafeClass") ?
                ObjectInputFilter.Status.ALLOWED : ObjectInputFilter.Status.REJECTED;
        }
        return ObjectInputFilter.Status.UNDECIDED;
    });
    return ois.readObject();
}
```
**Why it's correct:** ObjectInputFilter restricts deserialization to safe classes.

## Binary Eval Assertions
- [ ] Detects pickle deserialization in eval case 1
- [ ] Detects Java deserialization in eval case 2
- [ ] Detects PHP unserialize in eval case 3
- [ ] Does NOT flag counter-example 1 (JSON)
- [ ] Does NOT flag counter-example 2 (ObjectInputFilter)
- [ ] Finding references OWASP Deserialization Cheat Sheet
- [ ] Severity assigned as critical
