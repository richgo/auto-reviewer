---
name: data pii exposure
description: >
  PII / Sensitive Data Exposure. Use this skill whenever
  diffs may introduce data issues on all, especially in all. Actively look for: Personal
  identifiable information (email, SSN, phone, address, health data) or sensitive data
  (passwords, tokens) leaked through API responses,... and report findings with critical
  severity expectations and actionable fixes.
---

# PII / Sensitive Data Exposure
## Task Metadata
- Category: `data`
- Severity: `critical`
- Platforms: `all`
- Languages: `all`

## Purpose
Personal identifiable information (email, SSN, phone, address, health data) or sensitive data (passwords, tokens) leaked through API responses, logs, error messages, or analytics.

## Detection Heuristics
- API responses including fields like `password`, `ssn`, `creditCard` even if hashed
- User objects serialized without field filtering (returning full model)
- PII in log statements (email, phone, IP in structured logs)
- Error messages containing user data or stack traces with PII
- Analytics events with PII fields

## Eval Cases
### Case 1: Full user object in API response
```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user); // includes passwordHash, ssn, etc.
});
```
**Expected finding:** Critical — PII exposure. Full user model returned including sensitive fields. Select only needed fields or use a DTO/serializer.

### Case 2: PII in logs
```python
logger.info(f"User registered: {user.email}, phone: {user.phone}, SSN: {user.ssn}")
```
**Expected finding:** Critical — PII logged. SSN and phone number written to logs. Redact or mask sensitive fields.

## Counter-Examples
### Counter 1: DTO/projection
```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id).select('name email avatar');
  res.json(user);
});
```
**Why it's correct:** Only non-sensitive fields selected.

## Binary Eval Assertions
- [ ] Detects PII in API response in eval case 1
- [ ] Detects PII in logs in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies specific sensitive fields
- [ ] Severity assigned as critical
