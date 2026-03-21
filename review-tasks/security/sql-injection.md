# Task: SQL Injection

## Category
security

## Severity
critical

## Platforms
web, api

## Languages
all

## Description
User-controlled input concatenated or interpolated directly into SQL queries, allowing attackers to manipulate query logic, extract data, or modify/delete records.

## Detection Heuristics
- String concatenation or f-string interpolation inside SQL query strings
- Raw SQL with user input not passed through parameterized queries
- ORM `.raw()` or `.execute()` calls with string formatting
- Dynamic table/column names from user input without allowlist validation

## Eval Cases

### Case 1: Python f-string SQL
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()
```
**Expected finding:** Critical — SQL injection via f-string interpolation. User input `username` is directly embedded in query. Use parameterized query: `cursor.execute("SELECT * FROM users WHERE username = %s", (username,))`

### Case 2: Node.js template literal
```javascript
app.get('/users', (req, res) => {
  const query = `SELECT * FROM users WHERE role = '${req.query.role}'`;
  db.query(query, (err, results) => {
    res.json(results);
  });
});
```
**Expected finding:** Critical — SQL injection via template literal. Use parameterized query: `db.query('SELECT * FROM users WHERE role = ?', [req.query.role])`

### Case 3: Java string concatenation
```java
String query = "SELECT * FROM orders WHERE status = '" + request.getParameter("status") + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```
**Expected finding:** Critical — SQL injection via string concatenation. Use PreparedStatement with parameter binding.

## Counter-Examples

### Counter 1: Parameterized query
```python
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()
```
**Why it's correct:** Uses parameterized query — the database driver handles escaping.

### Counter 2: ORM query builder
```python
user = User.objects.filter(username=username).first()
```
**Why it's correct:** Django ORM parameterizes automatically.

## Binary Eval Assertions
- [ ] Detects SQL injection in eval case 1 (Python f-string)
- [ ] Detects SQL injection in eval case 2 (Node.js template literal)
- [ ] Detects SQL injection in eval case 3 (Java concatenation)
- [ ] Does NOT flag counter-example 1 (parameterized query)
- [ ] Does NOT flag counter-example 2 (ORM query)
- [ ] Finding includes fix suggestion with parameterized query
- [ ] Severity assigned as critical
