---
name: security cicd security
description: >
  CI/CD Security Issues. Use this skill whenever diffs
  may introduce security issues on all, especially in YAML, Groovy, all. Actively look
  for: CI/CD security issues include secrets in pipeline files, overly permissive
  workflows, missing code signing, unvalidated third-party actions, and... and report
  findings with high severity expectations and actionable fixes.
---

# CI/CD Security Issues
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `all`
- Languages: `YAML, Groovy, all`

## Purpose
CI/CD security issues include secrets in pipeline files, overly permissive workflows, missing code signing, unvalidated third-party actions, and lack of supply chain security controls (SBOM, provenance).

## Detection Heuristics
- Secrets hardcoded in .github/workflows, .gitlab-ci.yml, Jenkinsfile
- Workflows triggered on pull_request_target without approval
- Third-party GitHub Actions not pinned to SHA
- Missing artifact signing or SBOM generation
- No dependency scanning in CI pipeline
- Overpermissioned GITHUB_TOKEN or service accounts

## Eval Cases
### Case 1: Hardcoded secret in workflow
```yaml
# .github/workflows/deploy.yml - BUGGY CODE
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          API_KEY: sk-proj-xxxxxxxxxxxxxx # Hardcoded!
        run: ./deploy.sh
```
**Expected finding:** Critical — API key hardcoded in workflow file. Visible in version control history. Use GitHub encrypted secrets: `${{ secrets.API_KEY }}`.

### Case 2: Unpinned third-party action
```yaml
# BUGGY CODE — should be detected
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - uses: some-org/deploy-action@main # Branch, not SHA!
```
**Expected finding:** Medium — Third-party action pinned to `@main` branch. Maintainer can push malicious code. Pin to full SHA: `@a1b2c3d4...` or use trusted actions only.

### Case 3: pull_request_target without protection
```yaml
# BUGGY CODE — should be detected
on:
  pull_request_target:
    types: [opened]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm install && npm test
```
**Expected finding:** High — pull_request_target allows untrusted PRs to run with write access to secrets. Attacker can modify package.json to exfiltrate secrets. Use pull_request for untrusted code or require manual approval.

## Counter-Examples
### Counter 1: Secrets from environment
```yaml
# CORRECT CODE — should NOT be flagged
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh
```
**Why it's correct:** Secret stored in GitHub Secrets, not in file.

### Counter 2: Pinned action SHA
```yaml
# CORRECT CODE — should NOT be flagged
jobs:
  build:
    steps:
      - uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0
```
**Why it's correct:** Action pinned to specific commit SHA with version comment.

## Binary Eval Assertions
- [ ] Detects hardcoded secret in eval case 1
- [ ] Detects unpinned action in eval case 2
- [ ] Detects unsafe pull_request_target in eval case 3
- [ ] Does NOT flag counter-example 1 (GitHub Secrets)
- [ ] Does NOT flag counter-example 2 (pinned SHA)
- [ ] Finding references OWASP CI/CD Security Cheat Sheet
- [ ] Severity assigned as high or critical for secrets
