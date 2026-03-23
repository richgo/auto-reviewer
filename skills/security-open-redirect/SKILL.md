---
name: review-task-security-open-redirect
description: >
  Migrated review-task skill for Open Redirect. Use this skill whenever diffs may
  introduce security issues on web, api, especially in all. Actively look for: Open
  redirect vulnerabilities occur when user-controlled input determines the target of a
  redirect without validation, allowing attackers to... and report findings with medium
  severity expectations and actionable fixes.
---

# Open Redirect

## Source Lineage
- Original review task: `review-tasks/security/open-redirect.md`
- Migrated skill artifact: `skills/review-task-security-open-redirect/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Open redirect vulnerabilities occur when user-controlled input determines the target of a redirect without validation, allowing attackers to craft phishing URLs that appear to come from trusted domains but redirect to malicious sites.

## Detection Heuristics
- Redirect/Location header set from user input (query param, POST body)
- Missing URL validation or allowlist checking before redirect
- Accepting full URLs instead of relative paths
- No origin/domain validation on redirect targets
- OAuth/SAML redirect_uri not validated against registered URIs

## Eval Cases
### Case 1: Unvalidated query parameter redirect
```python
# BUGGY CODE — should be detected
@app.route('/redirect')
def redirect_handler():
    target = request.args.get('url')
    return redirect(target)
```
**Expected finding:** Medium — Open redirect via unvalidated URL parameter. Attacker can craft `https://trusted.com/redirect?url=https://evil.com` for phishing. Validate target against allowlist or use relative paths only.

### Case 2: POST-based redirect without validation
```javascript
// BUGGY CODE — should be detected
app.post('/logout', (req, res) => {
  req.session.destroy();
  const returnUrl = req.body.returnUrl;
  res.redirect(returnUrl);
});
```
**Expected finding:** Medium — Open redirect from POST body. No validation on `returnUrl` allows phishing attacks. Validate against allowlist: `['/home', '/login']` or check URL starts with `/` and doesn't contain `//`.

### Case 3: Header injection via Location
```java
// BUGGY CODE — should be detected
@GetMapping("/goto")
public void redirect(@RequestParam String url, HttpServletResponse response) throws IOException {
    response.setHeader("Location", url);
    response.setStatus(302);
}
```
**Expected finding:** High — Unvalidated redirect with header injection risk. Attacker can inject CRLF characters to manipulate headers. Validate URL format and use `response.sendRedirect()` with allowlist-checked URLs only.

## Counter-Examples
### Counter 1: Allowlist-based redirect
```python
# CORRECT CODE — should NOT be flagged
ALLOWED_REDIRECTS = ['/dashboard', '/profile', '/settings']

@app.route('/redirect')
def redirect_handler():
    target = request.args.get('url', '/') 
    if target not in ALLOWED_REDIRECTS:
        target = '/'
    return redirect(target)
```
**Why it's correct:** Redirect targets validated against strict allowlist.

### Counter 2: Relative path validation
```javascript
// CORRECT CODE — should NOT be flagged
app.post('/logout', (req, res) => {
  req.session.destroy();
  let returnUrl = req.body.returnUrl || '/';
  // Ensure relative path, no protocol
  if (!returnUrl.startsWith('/') || returnUrl.startsWith('//')) {
    returnUrl = '/';
  }
  res.redirect(returnUrl);
});
```
**Why it's correct:** Validates redirect is relative path starting with single `/`, blocks protocol-relative URLs `//evil.com`.

## Binary Eval Assertions
- [ ] Detects open redirect in eval case 1 (query param)
- [ ] Detects open redirect in eval case 2 (POST body)
- [ ] Detects header injection risk in eval case 3
- [ ] Does NOT flag counter-example 1 (allowlist validation)
- [ ] Does NOT flag counter-example 2 (relative path check)
- [ ] Finding recommends allowlist or relative path validation
- [ ] Severity assigned as medium (high if combined with CRLF injection)

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
