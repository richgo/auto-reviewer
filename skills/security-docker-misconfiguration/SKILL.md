---
name: review-task-security-docker-misconfiguration
description: >
  Migrated review-task skill for Docker Misconfiguration. Use this skill whenever diffs
  may introduce security issues on all, especially in Dockerfile, all. Actively look
  for: Docker security misconfigurations include running containers as root, exposing
  unnecessary ports, missing resource limits, using `latest` tags, insecure... and
  report findings with high severity expectations and actionable fixes.
---

# Docker Misconfiguration

## Source Lineage
- Original review task: `review-tasks/security/docker-misconfiguration.md`
- Migrated skill artifact: `skills/review-task-security-docker-misconfiguration/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `all`
- Languages: `Dockerfile, all`

## Purpose
Docker security misconfigurations include running containers as root, exposing unnecessary ports, missing resource limits, using `latest` tags, insecure base images, secrets in images, and overly permissive volume mounts.

## Detection Heuristics
- `USER root` or missing `USER` directive (runs as root)
- Exposed ports not documented or excessive (`EXPOSE 0-65535`)
- Missing resource limits (memory, CPU)
- `FROM image:latest` instead of pinned versions
- Secrets in Dockerfile (`ENV API_KEY=xxx`, `COPY secret.key`)
- Bind mounts to sensitive host paths (`-v /:/host`)
- `--privileged` flag or dangerous capabilities

## Eval Cases
### Case 1: Running as root
```dockerfile
# BUGGY CODE — should be detected
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```
**Expected finding:** High — Container runs as root (no USER directive). If container compromised, attacker has root access. Add non-root user: `RUN adduser -D appuser && chown -R appuser /app` then `USER appuser`.

### Case 2: Secrets in environment variables
```dockerfile
# BUGGY CODE — should be detected
FROM python:3.11
ENV DATABASE_PASSWORD=supersecret123
ENV API_KEY=sk-proj-xxxxxxxxxxxx
COPY app.py /app/
CMD ["python", "/app/app.py"]
```
**Expected finding:** Critical — Secrets hardcoded in Dockerfile environment variables. Visible in image layers and `docker inspect`. Use Docker secrets, Kubernetes secrets, or environment variables passed at runtime: `docker run -e DATABASE_PASSWORD=...`.

### Case 3: Latest tag and no resource limits
```yaml
# docker-compose.yml - BUGGY CODE
services:
  app:
    image: node:latest # Unpinned tag
    # No resource limits
```
**Expected finding:** Medium — Using `:latest` tag (unpredictable updates) and no resource limits. Pin to specific version `node:18.19.0`. Add limits: `mem_limit: 512m`, `cpus: 0.5`.

## Counter-Examples
### Counter 1: Non-root user with pinned base
```dockerfile
# CORRECT CODE — should NOT be flagged
FROM node:18.19.0-alpine
RUN addgroup -g 1001 appgroup && adduser -D -u 1001 -G appgroup appuser
WORKDIR /app
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```
**Why it's correct:** Pinned base image, runs as non-root user, ownership properly set.

### Counter 2: Secrets from runtime environment
```dockerfile
# CORRECT CODE — should NOT be flagged
FROM python:3.11-slim
RUN useradd -m appuser
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app.py ./
USER appuser
# Secrets passed at runtime via -e or Docker secrets
CMD ["python", "app.py"]
```
**Why it's correct:** No hardcoded secrets, non-root user, slim base image.

## Binary Eval Assertions
- [ ] Detects root user in eval case 1
- [ ] Detects hardcoded secrets in eval case 2
- [ ] Detects latest tag in eval case 3
- [ ] Does NOT flag counter-example 1 (non-root + pinned)
- [ ] Does NOT flag counter-example 2 (runtime secrets)
- [ ] Finding references OWASP Docker Security Cheat Sheet
- [ ] Severity assigned as high for root or hardcoded secrets

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
