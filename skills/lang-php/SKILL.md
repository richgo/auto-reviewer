---
name: lang-php
description: >
  PHP-specific code review: Laravel/Symfony security, SQL injection patterns, file inclusion, type
  juggling, OWASP PHP cheat sheets. Trigger when reviewing PHP (.php) files, especially Laravel,
  Symfony, or WordPress applications.
---

# Language-Specific Review: PHP

## Purpose
PHP-specific guidance: framework security, injection vulnerabilities, and PHP-specific pitfalls.

## Key Areas

### 1. SQL Injection
```php
// ❌ UNSAFE: String concatenation
$query = "SELECT * FROM users WHERE email = '" . $_POST['email'] . "'";
mysqli_query($conn, $query);

// ✅ SAFE: Prepared statements
$stmt = $conn->prepare("SELECT * FROM users WHERE email = ?");
$stmt->bind_param("s", $_POST['email']);
$stmt->execute();
```

### 2. File Inclusion
```php
// ❌ UNSAFE: User input in include
include($_GET['page'] . '.php');  // LFI/RFI

// ✅ SAFE: Whitelist
$allowed = ['home', 'about', 'contact'];
$page = $_GET['page'] ?? 'home';
if (in_array($page, $allowed, true)) {
    include($page . '.php');
}
```

### 3. Type Juggling
```php
// ❌ UNSAFE: Loose comparison
if ($_POST['token'] == $expected) {  // "0e123" == "0e456" is true!
    // Authenticated
}

// ✅ SAFE: Strict comparison
if ($_POST['token'] === $expected) {
    // Authenticated
}
```

### 4. Command Injection
```php
// ❌ UNSAFE: Shell execution
shell_exec("ping -c 4 " . $_POST['host']);

// ✅ SAFE: escapeshellarg
shell_exec("ping -c 4 " . escapeshellarg($_POST['host']));

// ✅ BETTER: Avoid shell
// Use PHP functions like gethostbyname()
```

### 5. XSS in Templates
```php
<!-- ❌ UNSAFE: Unescaped -->
<?= $user_bio ?>

<!-- ✅ SAFE: htmlspecialchars -->
<?= htmlspecialchars($user_bio, ENT_QUOTES, 'UTF-8') ?>

<!-- Laravel Blade auto-escapes: -->
{{ $user_bio }}
```

### 6. Laravel Security
```php
// ❌ UNSAFE: Raw query
DB::select("SELECT * FROM users WHERE id = " . $id);

// ✅ SAFE: Query builder
DB::table('users')->where('id', $id)->get();

// ❌ UNSAFE: Mass assignment
$user = User::create($request->all());

// ✅ SAFE: Fillable
class User extends Model {
    protected $fillable = ['name', 'email'];
}
```

## OWASP References
- [PHP Configuration](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html)

## Quick Checklist
- [ ] Prepared statements for SQL
- [ ] Whitelist for file inclusion
- [ ] Strict comparison (===) not loose (==)
- [ ] escapeshellarg for command execution
- [ ] htmlspecialchars for HTML output
- [ ] Laravel fillable/guarded for models
