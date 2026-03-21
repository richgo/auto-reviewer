# Task: NoSQL Injection

## Category
security

## Severity
high

## Platforms
all

## Languages
JavaScript, TypeScript, Python, Java

## Description
NoSQL injection occurs when user input is passed unsanitized to NoSQL query operators, allowing attackers to manipulate query logic, bypass authentication, extract data, or execute arbitrary JavaScript in databases like MongoDB.

## Detection Heuristics
- Direct user input in MongoDB query objects without validation
- Use of $where operator with user-controlled strings
- JSON.parse() of user input used in queries
- Missing type validation (e.g., accepting objects when expecting strings)
- Unsanitized user input in aggregation pipelines or map-reduce functions

## Eval Cases

### Case 1: MongoDB authentication bypass
```javascript
// BUGGY CODE — should be detected
const username = req.body.username;
const password = req.body.password;
const user = await db.collection('users').findOne({
  username: username,
  password: password
});
```
**Expected finding:** High — NoSQL injection via object injection. Attacker can send `{"username": {"$ne": null}, "password": {"$ne": null}}` to bypass authentication. Validate input types and use strict equality checks.

### Case 2: Python PyMongo $where injection
```python
# BUGGY CODE — should be detected
user_filter = request.json.get('filter')
results = db.products.find({'$where': f'this.price < {user_filter}'})
```
**Expected finding:** Critical — NoSQL injection via $where. User input flows to JavaScript execution context in MongoDB. Attacker can inject arbitrary JS: `0; while(true){}` for DoS. Never use $where with user input.

### Case 3: MongoDB aggregation injection
```javascript
// BUGGY CODE — should be detected
const category = req.query.category;
const pipeline = [
  { $match: { category: category } },
  { $group: { _id: '$category', count: { $sum: 1 } } }
];
db.collection('items').aggregate(pipeline);
```
**Expected finding:** High — NoSQL injection in aggregation pipeline. User-controlled `category` allows injection of operators like `{"$gt": ""}` to match all documents. Sanitize or validate against allowlist.

## Counter-Examples

### Counter 1: Type validation before query
```javascript
// CORRECT CODE — should NOT be flagged
const username = req.body.username;
const password = req.body.password;
if (typeof username !== 'string' || typeof password !== 'string') {
  return res.status(400).send('Invalid input');
}
const user = await db.collection('users').findOne({
  username: username,
  password: password
});
```
**Why it's correct:** Type validation ensures no object injection is possible.

### Counter 2: Parameterized query with sanitization
```python
# CORRECT CODE — should NOT be flagged
import re
category = request.json.get('category')
if not re.match(r'^[a-zA-Z0-9_]+$', category):
    abort(400)
results = db.products.find({'category': category})
```
**Why it's correct:** Input validation with allowlist pattern prevents operator injection.

## Binary Eval Assertions
- [ ] Detects NoSQL injection in eval case 1 (authentication bypass)
- [ ] Detects NoSQL injection in eval case 2 ($where with user input)
- [ ] Detects NoSQL injection in eval case 3 (aggregation pipeline)
- [ ] Does NOT flag counter-example 1 (type validation)
- [ ] Does NOT flag counter-example 2 (sanitized input)
- [ ] Finding warns about object injection and operator abuse
- [ ] Severity assigned as high or critical for $where usage
