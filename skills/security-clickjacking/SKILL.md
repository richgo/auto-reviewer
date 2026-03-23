---
name: review-task-security-clickjacking
description: >
  Migrated review-task skill for Clickjacking Vulnerabilities. Use this skill whenever
  diffs may introduce security issues on web, especially in all. Actively look for:
  Clickjacking (UI redressing) attacks trick users into clicking hidden elements by
  overlaying transparent iframes over legitimate UI. Prevention... and report findings
  with medium severity expectations and actionable fixes.
---

# Clickjacking Vulnerabilities

## Source Lineage
- Original review task: `review-tasks/security/clickjacking.md`
- Migrated skill artifact: `skills/review-task-security-clickjacking/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web`
- Languages: `all`

## Purpose
Clickjacking (UI redressing) attacks trick users into clicking hidden elements by overlaying transparent iframes over legitimate UI. Prevention requires X-Frame-Options header or CSP frame-ancestors directive.

## Detection Heuristics
- Missing X-Frame-Options header on pages with sensitive actions
- Missing CSP frame-ancestors directive
- X-Frame-Options set to ALLOW-FROM (deprecated, not widely supported)
- Framebusting JavaScript used instead of headers (unreliable)
- Sensitive pages (login, payment, settings) lacking iframe protection

## Eval Cases
### Case 1: No iframe protection on login page
```python
# BUGGY CODE — should be detected
@app.route('/login')
def login():
    return render_template('login.html')
# No X-Frame-Options or CSP header
```
**Expected finding:** Medium — Login page missing clickjacking protection. Page can be embedded in iframe on attacker's site to trick users into entering credentials. Add `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'`.

### Case 2: Relying on JavaScript framebusting
```javascript
// BUGGY CODE — should be detected
app.get('/settings', (req, res) => {
  res.send(`
    <html>
    <script>
      if (top !== self) {
        top.location = self.location; // Framebusting
      }
    </script>
    <body>Sensitive settings</body>
    </html>
  `);
});
```
**Expected finding:** Medium — JavaScript framebusting is unreliable. Can be bypassed with sandbox iframe attribute or double framing. Use HTTP headers: `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'`.

### Case 3: ALLOW-FROM usage (deprecated)
```java
// BUGGY CODE — should be detected
@GetMapping("/payment")
public String payment(HttpServletResponse response) {
    response.setHeader("X-Frame-Options", "ALLOW-FROM https://trusted.com");
    return "payment";
}
```
**Expected finding:** Medium — X-Frame-Options ALLOW-FROM is deprecated and not supported by modern browsers. Use CSP `frame-ancestors` instead: `Content-Security-Policy: frame-ancestors https://trusted.com`.

## Counter-Examples
### Counter 1: X-Frame-Options DENY
```python
# CORRECT CODE — should NOT be flagged
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/login')
def login():
    return render_template('login.html')
```
**Why it's correct:** X-Frame-Options DENY prevents all iframe embedding.

### Counter 2: CSP frame-ancestors
```javascript
// CORRECT CODE — should NOT be flagged
const helmet = require('helmet');
app.use(helmet.contentSecurityPolicy({
  directives: {
    frameAncestors: ["'none'"]
  }
}));

app.get('/settings', (req, res) => {
  res.send('<html><body>Sensitive settings</body></html>');
});
```
**Why it's correct:** CSP frame-ancestors 'none' blocks all iframe embedding with modern standard.

## Binary Eval Assertions
- [ ] Detects missing iframe protection in eval case 1
- [ ] Detects JavaScript framebusting in eval case 2
- [ ] Detects deprecated ALLOW-FROM in eval case 3
- [ ] Does NOT flag counter-example 1 (X-Frame-Options DENY)
- [ ] Does NOT flag counter-example 2 (CSP frame-ancestors)
- [ ] Finding recommends X-Frame-Options or CSP frame-ancestors
- [ ] Severity assigned as medium

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
