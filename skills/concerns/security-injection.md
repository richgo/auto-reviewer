---
name: security-injection
description: >
  Detect injection vulnerabilities in code review: SQL injection, XSS, command injection,
  LDAP injection, NoSQL injection, and DOM-based XSS. Trigger this skill when reviewing
  database queries, shell commands, HTML rendering, DOM manipulation, or any code that
  handles user input and passes it to interpreters. Critical for APIs, web applications,
  and any user-facing functionality.
---

# Security Review: Injection Vulnerabilities

## Purpose
Review code for injection vulnerabilities where user-controlled input flows unsanitized into interpreters (SQL, shell, HTML, DOM, LDAP, NoSQL). These are **critical and high-severity** bugs that enable attackers to bypass security controls, extract data, or execute arbitrary commands.

## Scope
This skill covers six major injection classes:
1. **SQL Injection** — user input in SQL queries
2. **Cross-Site Scripting (XSS)** — user input rendered in HTML
3. **DOM-Based XSS** — client-side JavaScript manipulating DOM with user input
4. **Command Injection** — user input in shell commands
5. **LDAP Injection** — user input in LDAP filters
6. **NoSQL Injection** — user input in NoSQL queries (MongoDB, etc.)

## Detection Strategy

### Universal Red Flags
Look for these patterns across all injection types:
- **String concatenation/interpolation** with user input
- **Unvalidated input** flowing to sensitive sinks
- **Bypass of framework protections** (e.g., `dangerouslySetInnerHTML`, `shell=True`)
- **Raw/unsafe** query methods instead of parameterized APIs
- **Dynamic construction** of code, queries, or commands from user data

### High-Risk Sinks by Type

**SQL Injection:**
- `cursor.execute(f"SELECT...")`
- `db.query(\`SELECT ${userInput}\`)`
- `Statement.executeQuery(query)`
- ORM `.raw()` or `.execute()` with string formatting

**XSS (Reflected/Stored):**
- `innerHTML`, `outerHTML`, `document.write()` with user input
- `dangerouslySetInnerHTML` without sanitization
- Template `{{ var | safe }}`, `{{{ var }}}`, `<%- var %>`
- URL params reflected in HTML response

**DOM XSS:**
- `element.innerHTML = location.hash`
- `eval(window.name)`, `new Function(userInput)`
- `document.write(decodeURIComponent(...))`
- Unsafe jQuery: `$(userInput)`, `$el.html(userInput)`

**Command Injection:**
- `subprocess.call(..., shell=True)` with user input
- `child_process.exec()` with template literals
- `Runtime.exec("cmd " + userInput)`
- `os.system(f"command {userInput}")`

**LDAP Injection:**
- `ldap.search_s(f"(uid={username})")`
- String formatting in LDAP filter construction

**NoSQL Injection:**
- `db.collection.find({ user: req.body.user })`
- `$where` clauses with user input
- Unvalidated object passed to query methods

## Platform-Specific Guidance

### Web/API
- **Primary risks:** SQL injection, XSS, command injection
- **Key review areas:** Route handlers, template rendering, database queries, shell executions
- **OWASP references:** SQL_Injection_Prevention, Cross_Site_Scripting_Prevention, OS_Command_Injection_Defense

### Android
- **Primary risks:** SQL injection (SQLite), command injection, XSS in WebView
- **Key review areas:** `WebView.loadUrl()`, `Runtime.exec()`, raw SQLite queries, `ContentProvider` SQL construction
- **Extra checks:** `WebView` with JavaScript enabled + user input

### iOS
- **Primary risks:** SQL injection (SQLite/Core Data), command injection, XSS in WKWebView
- **Key review areas:** `evaluateJavaScript()`, `Process()` calls, Core Data fetch predicates with string formatting
- **Extra checks:** URL scheme handlers passing input to shell

### Microservices
- **Primary risks:** SQL/NoSQL injection, command injection in sidecars/scripts
- **Key review areas:** Service-to-service query parameters, environment variable injection, orchestration scripts
- **Extra checks:** Dynamic container commands, injection through message queues

## Review Instructions

### Step 1: Identify User Input Sources
Trace data flow from:
- HTTP request parameters (query, body, headers, cookies)
- File uploads, WebSocket messages
- Database records (stored XSS)
- Environment variables (if user-controllable)
- Message queue payloads

### Step 2: Find Sensitive Sinks
Search for high-risk functions (see "High-Risk Sinks by Type" above).

### Step 3: Check Data Flow
For each sink:
1. **Trace backward:** Does user input reach this sink?
2. **Check sanitization:** Is there parameterization, escaping, or validation?
3. **Verify framework usage:** Is the safe API used (e.g., parameterized queries)?

### Step 4: Validate Fixes
Safe patterns to look for:
- **SQL:** Parameterized queries (`?` placeholders, not string formatting)
- **XSS:** Auto-escaping templates, `textContent`, DOMPurify sanitization
- **DOM XSS:** Avoid `innerHTML` with user data; use `textContent` or sanitize
- **Command:** `shell=False` with argument lists, `execFile()` instead of `exec()`
- **LDAP:** Escape special chars `* ( ) \ NUL` or use parameterized binds
- **NoSQL:** Schema validation, avoid `$where`, cast types explicitly

### Step 5: Report Findings
For each injection vulnerability:
- **Severity:** Critical (SQL, command, LDAP), High (XSS, NoSQL, DOM XSS)
- **Location:** File, line number, function name
- **Description:** "User input `<var>` flows unsanitized to `<sink>`, enabling `<attack>`"
- **Fix:** Specific remediation (e.g., "Use parameterized query: `cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))`")
- **Reference:** Link to OWASP cheat sheet

## Examples

### ✅ SAFE: Parameterized SQL Query (Python)
```python
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

### ❌ UNSAFE: String Interpolation (Python)
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```
**Finding:** Critical — SQL injection via f-string. Attacker can inject `' OR '1'='1`.

### ✅ SAFE: React Auto-Escaping
```jsx
<div>{comment}</div>
```

### ❌ UNSAFE: dangerouslySetInnerHTML
```jsx
<div dangerouslySetInnerHTML={{ __html: comment }} />
```
**Finding:** High — XSS via dangerouslySetInnerHTML. Sanitize with DOMPurify first.

### ✅ SAFE: Argument List (Node.js)
```javascript
execFile('ping', ['-c', '4', userInput], callback);
```

### ❌ UNSAFE: String Concatenation (Node.js)
```javascript
exec(`ping -c 4 ${userInput}`, callback);
```
**Finding:** Critical — Command injection. Attacker can inject `8.8.8.8; rm -rf /`.

## Related Review Tasks
Detailed detection guidance for each injection type:
- `review-tasks/security/sql-injection.md`
- `review-tasks/security/xss.md`
- `review-tasks/security/dom-xss.md`
- `review-tasks/security/command-injection.md`
- `review-tasks/security/ldap-injection.md`
- `review-tasks/security/nosql-injection.md`

## OWASP References
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOM based XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [OS Command Injection Defense](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
- [LDAP Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html)
- [Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

## Quick Checklist
- [ ] User input traced from source to sink
- [ ] All SQL queries use parameterized statements
- [ ] No `innerHTML`/`dangerouslySetInnerHTML` with user data (or sanitized)
- [ ] Shell commands use argument arrays, not string concatenation
- [ ] Template engines use auto-escaping (no `| safe` on user data)
- [ ] NoSQL queries validate/cast types, avoid `$where`
- [ ] LDAP filters escape special characters
