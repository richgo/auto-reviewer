---
name: security oauth misconfiguration
description: >
  OAuth/SAML Misconfiguration. Use this skill whenever
  diffs may introduce security issues on web, api, especially in all. Actively look for:
  OAuth and SAML misconfigurations include missing state parameter validation, insecure
  redirect URIs, weak JWT signatures, accepting unsigned SAML... and report findings
  with high severity expectations and actionable fixes.
---

# OAuth/SAML Misconfiguration
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
OAuth and SAML misconfigurations include missing state parameter validation, insecure redirect URIs, weak JWT signatures, accepting unsigned SAML assertions, and improper token validation leading to account takeover.

## Detection Heuristics
- Missing or unvalidated state parameter in OAuth flows (CSRF protection)
- Wildcard or missing redirect_uri validation
- JWT tokens not verified or using algorithm=none
- SAML assertions accepted without signature verification
- Missing nonce validation in OpenID Connect
- Accepting tokens from untrusted issuers

## Eval Cases
### Case 1: Missing OAuth state validation
```python
# BUGGY CODE — should be detected
@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    # Missing state validation
    token_response = requests.post('https://oauth.provider/token', data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    access_token = token_response.json()['access_token']
    session['access_token'] = access_token
    return redirect('/dashboard')
```
**Expected finding:** High — Missing OAuth state parameter validation. Vulnerable to CSRF attacks where attacker can link victim's account to attacker's OAuth provider account. Generate random state before redirect, validate on callback.

### Case 2: Insecure JWT verification
```javascript
// BUGGY CODE — should be detected
const jwt = require('jsonwebtoken');
app.post('/api/auth', (req, res) => {
  const token = req.body.token;
  const decoded = jwt.decode(token); // No verification!
  req.session.userId = decoded.sub;
  res.json({ success: true });
});
```
**Expected finding:** Critical — JWT accepted without signature verification. Attacker can forge tokens with arbitrary claims. Use `jwt.verify(token, publicKey, { algorithms: ['RS256'] })` to validate signature and issuer.

### Case 3: Open redirect_uri in OAuth
```java
// BUGGY CODE — should be detected
@GetMapping("/oauth/authorize")
public String authorize(@RequestParam String redirect_uri, @RequestParam String client_id) {
    // No redirect_uri validation
    OAuthCode code = generateAuthCode(client_id);
    return "redirect:" + redirect_uri + "?code=" + code.getValue();
}
```
**Expected finding:** Critical — Unvalidated OAuth redirect_uri. Attacker can steal authorization code by setting redirect_uri to malicious domain. Validate redirect_uri against pre-registered allowlist for each client_id.

## Counter-Examples
### Counter 1: Proper OAuth state validation
```python
# CORRECT CODE — should NOT be flagged
import secrets
@app.route('/oauth/login')
def oauth_login():
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    return redirect(f'https://oauth.provider/authorize?client_id={CLIENT_ID}&state={state}')

@app.route('/oauth/callback')
def oauth_callback():
    if request.args.get('state') != session.pop('oauth_state', None):
        abort(403, 'Invalid state parameter')
    code = request.args.get('code')
    # ... proceed with token exchange
```
**Why it's correct:** State parameter generated, stored in session, validated on callback (CSRF protection).

### Counter 2: Secure JWT validation
```javascript
// CORRECT CODE — should NOT be flagged
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

const client = jwksClient({ jwksUri: 'https://oauth.provider/.well-known/jwks.json' });

app.post('/api/auth', async (req, res) => {
  try {
    const token = req.body.token;
    const decoded = jwt.verify(token, getKey, {
      algorithms: ['RS256'],
      issuer: 'https://oauth.provider',
      audience: CLIENT_ID
    });
    req.session.userId = decoded.sub;
    res.json({ success: true });
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
});
```
**Why it's correct:** JWT signature, issuer, audience, and algorithm validated against JWKS.

## Binary Eval Assertions
- [ ] Detects missing state validation in eval case 1
- [ ] Detects unverified JWT in eval case 2
- [ ] Detects open redirect_uri in eval case 3
- [ ] Does NOT flag counter-example 1 (state validation)
- [ ] Does NOT flag counter-example 2 (secure JWT verification)
- [ ] Finding references OWASP OAuth2/JWT/SAML cheat sheets
- [ ] Severity assigned as high or critical
