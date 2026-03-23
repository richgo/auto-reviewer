---
name: security dom xss
description: >
  Migrated review-task skill for DOM-based XSS. Use this skill whenever diffs may
  introduce security issues on web, especially in JavaScript, TypeScript. Actively look
  for: DOM-based Cross-Site Scripting occurs when user-controlled data flows into
  dangerous JavaScript DOM sinks (innerHTML, document.write, eval) without
  sanitization,... and report findings with high severity expectations and actionable
  fixes.
---

# DOM-based XSS

## Source Lineage
- Original review task: `review-tasks/security/dom-xss.md`
- Migrated skill artifact: `skills/review-task-security-dom-xss/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web`
- Languages: `JavaScript, TypeScript`

## Purpose
DOM-based Cross-Site Scripting occurs when user-controlled data flows into dangerous JavaScript DOM sinks (innerHTML, document.write, eval) without sanitization, allowing attackers to execute arbitrary JavaScript in the context of the application.

## Detection Heuristics
- User input assigned to dangerous DOM sinks: innerHTML, outerHTML, document.write, insertAdjacentHTML
- eval(), Function(), setTimeout/setInterval with string arguments from user data
- Location-based sources (location.hash, location.search) used in DOM manipulation without encoding
- jQuery html(), append(), prepend() with unsanitized user input
- Missing Content Security Policy or CSP with unsafe-inline/unsafe-eval

## Eval Cases
### Case 1: innerHTML with URL parameter
```javascript
// BUGGY CODE — should be detected
const params = new URLSearchParams(window.location.search);
const username = params.get('user');
document.getElementById('greeting').innerHTML = `Welcome, ${username}!`;
```
**Expected finding:** High — DOM XSS via innerHTML. User-controlled `username` from URL parameter flows to innerHTML sink. Attacker can inject `<img src=x onerror=alert(1)>`. Use textContent or DOMPurify.sanitize().

### Case 2: eval with location.hash
```javascript
// BUGGY CODE — should be detected
const command = location.hash.substring(1);
eval(command); // execute command from URL fragment
```
**Expected finding:** Critical — DOM XSS via eval(). URL fragment flows directly to eval(), allowing arbitrary code execution. Never use eval() with user input. Use safe parsing alternatives.

### Case 3: jQuery .html() with form input
```typescript
// BUGGY CODE — should be detected
$('#message-display').html(userMessage);
```
**Expected finding:** High — DOM XSS via jQuery .html(). User-controlled `userMessage` rendered as HTML. Use .text() for plain text or sanitize with DOMPurify before .html().

## Counter-Examples
### Counter 1: textContent for user data
```javascript
// CORRECT CODE — should NOT be flagged
const params = new URLSearchParams(window.location.search);
const username = params.get('user');
document.getElementById('greeting').textContent = `Welcome, ${username}!`;
```
**Why it's correct:** textContent automatically escapes HTML, preventing script execution.

### Counter 2: DOMPurify sanitization before innerHTML
```javascript
// CORRECT CODE — should NOT be flagged
import DOMPurify from 'dompurify';
document.getElementById('content').innerHTML = DOMPurify.sanitize(userInput);
```
**Why it's correct:** DOMPurify removes dangerous tags/attributes before rendering.

## Binary Eval Assertions
- [ ] Detects DOM XSS in eval case 1 (innerHTML with URL param)
- [ ] Detects DOM XSS in eval case 2 (eval with location.hash)
- [ ] Detects DOM XSS in eval case 3 (jQuery .html() with user input)
- [ ] Does NOT flag counter-example 1 (textContent)
- [ ] Does NOT flag counter-example 2 (DOMPurify sanitization)
- [ ] Finding includes sink location and data flow source
- [ ] Severity assigned as high or critical based on sink danger

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
