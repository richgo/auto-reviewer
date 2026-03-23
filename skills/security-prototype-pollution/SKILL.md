---
name: security prototype pollution
description: >
  Migrated review-task skill for Prototype Pollution. Use this skill whenever diffs may
  introduce security issues on web, api, especially in JavaScript, TypeScript. Actively
  look for: Prototype pollution occurs when attacker-controlled properties like
  `__proto__`, `constructor`, or `prototype` modify JavaScript object prototypes,
  leading to property... and report findings with high severity expectations and
  actionable fixes.
---

# Prototype Pollution

## Source Lineage
- Original review task: `review-tasks/security/prototype-pollution.md`
- Migrated skill artifact: `skills/review-task-security-prototype-pollution/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `JavaScript, TypeScript`

## Purpose
Prototype pollution occurs when attacker-controlled properties like `__proto__`, `constructor`, or `prototype` modify JavaScript object prototypes, leading to property injection, denial of service, or remote code execution in Node.js applications.

## Detection Heuristics
- Merging untrusted objects without key filtering (lodash merge, jQuery extend, Object.assign)
- Recursive object merging without `__proto__`/`constructor` blocklist
- Dynamic property assignment from user input: `obj[userKey] = value`
- Using vulnerable library versions (lodash < 4.17.21, minimist < 1.2.6)
- JSON.parse() followed by unvalidated object merge

## Eval Cases
### Case 1: Vulnerable lodash merge
```javascript
// BUGGY CODE — should be detected
const _ = require('lodash');
app.post('/update-config', (req, res) => {
  _.merge(appConfig, req.body);
  res.send('Config updated');
});
```
**Expected finding:** High — Prototype pollution via lodash merge. Attacker can send `{"__proto__": {"isAdmin": true}}` to pollute Object.prototype. Upgrade lodash >= 4.17.21 or use `_.mergeWith` with custom merge function filtering dangerous keys.

### Case 2: Unsafe recursive merge
```typescript
// BUGGY CODE — should be detected
function deepMerge(target: any, source: any): any {
  for (const key in source) {
    if (typeof source[key] === 'object') {
      target[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

app.post('/api/settings', (req, res) => {
  deepMerge(userSettings, req.body);
});
```
**Expected finding:** Critical — Unsafe recursive merge allows prototype pollution. No filtering of `__proto__`, `constructor`, or `prototype` keys. Add key blocklist check before merge or use Map instead of plain objects.

### Case 3: Dynamic property from query param
```javascript
// BUGGY CODE — should be detected
app.get('/api/user', (req, res) => {
  const user = {};
  const key = req.query.key;
  const value = req.query.value;
  user[key] = value;
  res.json(user);
});
```
**Expected finding:** High — Prototype pollution via dynamic property assignment. Request `?key=__proto__&value[isAdmin]=true` pollutes prototype. Validate key against allowlist or use Map for user-controlled keys.

## Counter-Examples
### Counter 1: Safe merge with key filtering
```javascript
// CORRECT CODE — should NOT be flagged
const BLOCKED_KEYS = ['__proto__', 'constructor', 'prototype'];

function safeMerge(target, source) {
  for (const key in source) {
    if (BLOCKED_KEYS.includes(key)) continue;
    if (source.hasOwnProperty(key)) {
      if (typeof source[key] === 'object' && source[key] !== null) {
        target[key] = safeMerge(target[key] || {}, source[key]);
      } else {
        target[key] = source[key];
      }
    }
  }
  return target;
}
```
**Why it's correct:** Blocks dangerous keys before merge, uses hasOwnProperty check.

### Counter 2: Using Map for user-controlled data
```javascript
// CORRECT CODE — should NOT be flagged
app.post('/api/settings', (req, res) => {
  const userSettings = new Map();
  for (const [key, value] of Object.entries(req.body)) {
    userSettings.set(key, value);
  }
  res.send('Settings saved');
});
```
**Why it's correct:** Map doesn't inherit from Object.prototype, immune to prototype pollution.

## Binary Eval Assertions
- [ ] Detects vulnerable lodash merge in eval case 1
- [ ] Detects unsafe recursive merge in eval case 2
- [ ] Detects dynamic property pollution in eval case 3
- [ ] Does NOT flag counter-example 1 (safe merge with filtering)
- [ ] Does NOT flag counter-example 2 (Map usage)
- [ ] Finding references OWASP Prototype Pollution Prevention
- [ ] Severity assigned as high or critical

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
