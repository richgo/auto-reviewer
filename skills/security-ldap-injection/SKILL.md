---
name: review-task-security-ldap-injection
description: >
  Migrated review-task skill for LDAP Injection. Use this skill whenever diffs may
  introduce security issues on all, especially in Java, C#, Python, PHP. Actively look
  for: LDAP injection occurs when user input is concatenated into LDAP filter strings
  without escaping, allowing attackers to manipulate... and report findings with high
  severity expectations and actionable fixes.
---

# LDAP Injection

## Source Lineage
- Original review task: `review-tasks/security/ldap-injection.md`
- Migrated skill artifact: `skills/review-task-security-ldap-injection/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `all`
- Languages: `Java, C#, Python, PHP`

## Purpose
LDAP injection occurs when user input is concatenated into LDAP filter strings without escaping, allowing attackers to manipulate query logic, bypass authentication, or extract sensitive directory data.

## Detection Heuristics
- String concatenation building LDAP filters with user input
- Missing LDAP filter escaping for special characters: * ( ) \ NUL
- Direct use of user input in authentication filters
- No input validation before LDAP query construction
- Absence of parameterized LDAP query APIs

## Eval Cases
### Case 1: Java LDAP authentication bypass
```java
// BUGGY CODE — should be detected
String username = request.getParameter("username");
String filter = "(&(uid=" + username + "))";
NamingEnumeration results = ctx.search("ou=users,dc=example,dc=com", filter, constraints);
```
**Expected finding:** High — LDAP injection in authentication filter. User-controlled `username` allows injection of `*)(uid=*))(|(uid=*` to bypass auth. Escape LDAP special characters using LdapEncoder or use parameterized queries.

### Case 2: Python ldap3 filter injection
```python
# BUGGY CODE — should be detected
from ldap3 import Server, Connection
username = request.form['username']
search_filter = f'(uid={username})'
conn.search('ou=users,dc=example,dc=com', search_filter, attributes=['cn', 'mail'])
```
**Expected finding:** High — LDAP injection via f-string. Inject `*)(objectClass=*)` to enumerate all directory objects. Use ldap3's safe filter construction or escape_filter_chars().

### Case 3: C# DirectorySearcher injection
```csharp
// BUGGY CODE — should be detected
string dept = Request.QueryString["department"];
DirectorySearcher searcher = new DirectorySearcher();
searcher.Filter = "(department=" + dept + ")";
SearchResultCollection results = searcher.FindAll();
```
**Expected finding:** High — LDAP injection in DirectorySearcher filter. User input `dept` not escaped. Use LdapEncoder.FilterEncode() before concatenation.

## Counter-Examples
### Counter 1: Escaped LDAP filter
```java
// CORRECT CODE — should NOT be flagged
import org.owasp.encoder.Encode;
String username = request.getParameter("username");
String safeUsername = Encode.forLdapFilter(username);
String filter = "(&(uid=" + safeUsername + "))";
ctx.search("ou=users,dc=example,dc=com", filter, constraints);
```
**Why it's correct:** OWASP Encoder escapes LDAP special characters before concatenation.

### Counter 2: ldap3 safe filter construction
```python
# CORRECT CODE — should NOT be flagged
from ldap3 import Server, Connection
from ldap3.utils.conv import escape_filter_chars
username = escape_filter_chars(request.form['username'])
search_filter = f'(uid={username})'
conn.search('ou=users,dc=example,dc=com', search_filter)
```
**Why it's correct:** escape_filter_chars() neutralizes LDAP metacharacters.

## Binary Eval Assertions
- [ ] Detects LDAP injection in eval case 1 (Java string concatenation)
- [ ] Detects LDAP injection in eval case 2 (Python f-string)
- [ ] Detects LDAP injection in eval case 3 (C# DirectorySearcher)
- [ ] Does NOT flag counter-example 1 (OWASP Encoder)
- [ ] Does NOT flag counter-example 2 (ldap3 escape_filter_chars)
- [ ] Finding references OWASP LDAP Injection Prevention guide
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
