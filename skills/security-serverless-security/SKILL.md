---
name: security serverless security
description: >
  Serverless Security Issues. Use this skill whenever
  diffs may introduce security issues on all, especially in all. Actively look for:
  Serverless security issues include overly permissive IAM roles, missing input
  validation, secrets in environment variables, insufficient logging, lack... and report
  findings with medium severity expectations and actionable fixes.
---

# Serverless Security Issues
## Task Metadata
- Category: `security`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Serverless security issues include overly permissive IAM roles, missing input validation, secrets in environment variables, insufficient logging, lack of function-level authorization, and unbounded execution times.

## Detection Heuristics
- Lambda/Cloud Function IAM roles with broad permissions
- Secrets in function environment variables (visible in console)
- No input validation on event triggers (S3, API Gateway)
- Missing function concurrency limits (cost amplification)
- No execution timeout or memory limits
- Lack of VPC isolation for functions accessing private resources

## Eval Cases
### Case 1: Overly permissive Lambda IAM role
```hcl
# BUGGY CODE — should be detected
resource "aws_iam_role_policy" "lambda" {
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "s3:*" # All S3 actions!
      Resource = "*"
    }]
  })
}
```
**Expected finding:** High — Lambda IAM role grants all S3 actions on all buckets. Compromised function can access/delete any S3 data. Scope to specific actions (s3:GetObject) and resources.

### Case 2: Secrets in environment variables
```javascript
// serverless.yml - BUGGY CODE
functions:
  api:
    handler: handler.main
    environment:
      DATABASE_PASSWORD: supersecret123 # Plaintext!
      STRIPE_KEY: sk_live_xxxxxx
```
**Expected finding:** Critical — Secrets stored as plaintext in function environment variables. Visible in Lambda console and CloudFormation. Use AWS Secrets Manager or Parameter Store with IAM-based access.

### Case 3: No input validation on S3 trigger
```python
# BUGGY CODE — should be detected
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        # No validation on key (could be path traversal)
        obj = s3.get_object(Bucket=bucket, Key=key)
        process_file(obj['Body'].read())
```
**Expected finding:** Medium — No validation on S3 object key. Malicious key like `../../../etc/passwd` could exploit path traversal in downstream processing. Validate file extensions and paths.

## Counter-Examples
### Counter 1: Scoped IAM policy
```hcl
# CORRECT CODE — should NOT be flagged
resource "aws_iam_role_policy" "lambda" {
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```
**Why it's correct:** IAM role scoped to read-only on specific bucket.

### Counter 2: Secrets from Secrets Manager
```javascript
// serverless.yml - CORRECT CODE
functions:
  api:
    handler: handler.main
    environment:
      SECRETS_ARN: arn:aws:secretsmanager:us-east-1:123456789012:secret:myapp
    iamRoleStatements:
      - Effect: Allow
        Action: secretsmanager:GetSecretValue
        Resource: arn:aws:secretsmanager:us-east-1:123456789012:secret:myapp
```
**Why it's correct:** Secrets retrieved at runtime from Secrets Manager, not hardcoded.

## Binary Eval Assertions
- [ ] Detects overly permissive IAM in eval case 1
- [ ] Detects plaintext secrets in eval case 2
- [ ] Detects missing input validation in eval case 3
- [ ] Does NOT flag counter-example 1 (scoped IAM)
- [ ] Does NOT flag counter-example 2 (Secrets Manager)
- [ ] Finding references OWASP Serverless Security
- [ ] Severity assigned as medium to high
