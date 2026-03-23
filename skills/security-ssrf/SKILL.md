---
name: review-task-security-ssrf
description: >
  Migrated review-task skill for Server-Side Request Forgery (SSRF). Use this skill
  whenever diffs may introduce security issues on web, api, especially in all. Actively
  look for: Application makes HTTP requests to URLs controlled by user input without
  validation, allowing attackers to access internal services,... and report findings
  with critical severity expectations and actionable fixes.
---

# Server-Side Request Forgery (SSRF)

## Source Lineage
- Original review task: `review-tasks/security/ssrf.md`
- Migrated skill artifact: `skills/review-task-security-ssrf/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Application makes HTTP requests to URLs controlled by user input without validation, allowing attackers to access internal services, cloud metadata endpoints, or bypass firewalls.

## Detection Heuristics
- HTTP client calls (fetch, requests, HttpClient) with user-supplied URLs
- URL parameters used to proxy/fetch remote resources
- Image/file download from user-provided URLs without allowlist
- Redirect URLs not validated against allowlist

## Eval Cases
### Case 1: Unvalidated URL fetch
```python
@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    response = requests.get(url)
    return response.content
```
**Expected finding:** Critical — SSRF. User-controlled URL passed directly to `requests.get()`. Attacker can access `http://169.254.169.254/` (cloud metadata) or internal services. Validate against URL allowlist.

### Case 2: Image fetch from user URL
```javascript
app.post('/avatar', async (req, res) => {
  const imageData = await fetch(req.body.imageUrl);
  await saveAvatar(await imageData.buffer());
  res.json({ success: true });
});
```
**Expected finding:** Critical — SSRF via image URL. Validate scheme (https only), hostname against allowlist, and block private IP ranges.

## Counter-Examples
### Counter 1: Allowlisted domains
```python
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_DOMAINS:
        abort(400)
    response = requests.get(url)
    return response.content
```
**Why it's correct:** URL validated against domain allowlist before fetching.

## Binary Eval Assertions
- [ ] Detects SSRF in eval case 1
- [ ] Detects SSRF in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding mentions cloud metadata / internal network risk
- [ ] Finding suggests allowlist-based validation
- [ ] Severity assigned as critical

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
