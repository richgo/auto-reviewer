---
name: security third party code
description: >
  Migrated review-task skill for Third-Party Code Security. Use this skill whenever
  diffs may introduce security issues on web, especially in JavaScript, TypeScript,
  HTML. Actively look for: Insecure third-party JavaScript and CSS integration can
  introduce XSS, data exfiltration, supply chain attacks, and privacy violations.
  Risks... and report findings with medium severity expectations and actionable fixes.
---

# Third-Party Code Security

## Source Lineage
- Original review task: `review-tasks/security/third-party-code.md`
- Migrated skill artifact: `skills/review-task-security-third-party-code/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `web`
- Languages: `JavaScript, TypeScript, HTML`

## Purpose
Insecure third-party JavaScript and CSS integration can introduce XSS, data exfiltration, supply chain attacks, and privacy violations. Risks include missing SRI, loading from untrusted CDNs, and lack of CSP restrictions.

## Detection Heuristics
- Script/link tags loading from CDN without Subresource Integrity (SRI)
- Third-party scripts included without CSP restrictions
- Inline script tags with untrusted source
- Loading analytics/ads without privacy review
- No Content-Security-Policy restricting script-src
- Using deprecated or unmaintained libraries

## Eval Cases
### Case 1: CDN script without SRI
```html
<!-- BUGGY CODE — should be detected -->
<script src="https://cdn.example.com/library.js"></script>
```
**Expected finding:** Medium — Third-party script loaded without Subresource Integrity. If CDN is compromised, malicious code executes on all pages. Add SRI hash: `<script src="..." integrity="sha384-..." crossorigin="anonymous"></script>`.

### Case 2: No CSP for third-party scripts
```python
# BUGGY CODE — should be detected
@app.route('/')
def index():
    return '''
    <html>
    <script src="https://analytics.example.com/track.js"></script>
    <body>Content</body>
    </html>
    '''
```
**Expected finding:** Medium — Third-party analytics script with no Content-Security-Policy. No restriction on what scripts can load or where they can send data. Implement CSP `script-src 'self' https://analytics.example.com; connect-src 'self' https://analytics.example.com`.

### Case 3: Loading untrusted inline script
```javascript
// BUGGY CODE — should be detected
app.get('/widget', (req, res) => {
  const widgetCode = req.query.code; // User-controlled
  res.send(`
    <html>
    <script>${widgetCode}</script>
    <body>Widget</body>
    </html>
  `);
});
```
**Expected finding:** Critical — User-controlled code in inline script tag. Direct XSS vulnerability. Never inject user input into script tags. Load widgets from trusted sources with SRI or use sandboxed iframes.

## Counter-Examples
### Counter 1: CDN with SRI and CSP
```html
<!-- CORRECT CODE — should NOT be flagged -->
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Security-Policy" 
        content="script-src 'self' https://cdn.example.com; default-src 'self'">
  <script src="https://cdn.example.com/library.js" 
          integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
          crossorigin="anonymous"></script>
</head>
<body>Content</body>
</html>
```
**Why it's correct:** SRI hash validates script integrity, CSP restricts allowed script sources.

### Counter 2: Sandboxed iframe for widgets
```javascript
// CORRECT CODE — should NOT be flagged
app.get('/widget', (req, res) => {
  const widgetUrl = req.query.url;
  // Validate URL against allowlist
  if (!ALLOWED_WIDGETS.includes(widgetUrl)) {
    return res.status(400).send('Invalid widget');
  }
  res.send(`
    <html>
    <iframe src="${widgetUrl}" sandbox="allow-scripts" style="border:0"></iframe>
    </html>
  `);
});
```
**Why it's correct:** Widget loaded in sandboxed iframe with limited permissions, URL validated.

## Binary Eval Assertions
- [ ] Detects CDN without SRI in eval case 1
- [ ] Detects missing CSP in eval case 2
- [ ] Detects inline script XSS in eval case 3
- [ ] Does NOT flag counter-example 1 (SRI + CSP)
- [ ] Does NOT flag counter-example 2 (sandboxed iframe)
- [ ] Finding recommends SRI and CSP script-src restrictions
- [ ] Severity assigned as medium (critical for direct XSS)

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
