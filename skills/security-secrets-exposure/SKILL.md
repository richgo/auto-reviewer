---
name: review-task-security-secrets-exposure
description: >
  Migrated review-task skill for Secrets/Credentials Exposure. Use this skill whenever
  diffs may introduce security issues on all, especially in all. Actively look for:
  Hardcoded secrets, API keys, passwords, or tokens in source code, config files
  committed to VCS, or logged/returned in... and report findings with critical severity
  expectations and actionable fixes.
---

# Secrets/Credentials Exposure

## Source Lineage
- Original review task: `review-tasks/security/secrets-exposure.md`
- Migrated skill artifact: `skills/review-task-security-secrets-exposure/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `all`
- Languages: `all`

## Purpose
Hardcoded secrets, API keys, passwords, or tokens in source code, config files committed to VCS, or logged/returned in responses.

## Detection Heuristics
- Hardcoded strings matching key patterns (AWS keys, JWT secrets, API tokens)
- `.env` files or credentials in committed config
- Secrets in log statements or error responses
- Private keys or certificates in source tree
- Connection strings with embedded passwords

## Eval Cases
### Case 1: Hardcoded API key
```python
STRIPE_SECRET_KEY = "sk_live_EXAMPLE_KEY_DO_NOT_USE"
stripe.api_key = STRIPE_SECRET_KEY
```
**Expected finding:** Critical — Hardcoded Stripe secret key in source code. Use environment variable: `os.environ['STRIPE_SECRET_KEY']`

### Case 2: Secret logged
```javascript
logger.info(`Authenticating with token: ${authToken}`);
```
**Expected finding:** High — Authentication token written to logs. Remove sensitive data from log output.

## Counter-Examples
### Counter 1: Environment variable
```python
stripe.api_key = os.environ['STRIPE_SECRET_KEY']
```
**Why it's correct:** Secret loaded from environment, not hardcoded.

## Binary Eval Assertions
- [ ] Detects hardcoded secret in eval case 1
- [ ] Detects logged secret in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding includes remediation (env var / secrets manager)
- [ ] Severity assigned as critical

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
