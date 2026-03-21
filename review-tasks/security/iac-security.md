# Task: Infrastructure as Code Security

## Category
security

## Severity
high

## Platforms
all

## Languages
Terraform, CloudFormation, Kubernetes YAML

## Description
IaC security issues include overly permissive IAM policies, public S3 buckets, unrestricted security groups, missing encryption, hardcoded secrets, and lack of policy-as-code validation (OPA, Checkov, tfsec).

## Detection Heuristics
- IAM policies with `Action: "*"` or `Resource: "*"`
- S3 buckets with `public-read` or `public-read-write` ACLs
- Security groups allowing `0.0.0.0/0` on sensitive ports (22, 3389, 3306)
- Missing encryption at rest (`encrypted = false`)
- Secrets in Terraform files or Kubernetes manifests
- No IaC scanning in CI (Checkov, tfsec, Terrascan)

## Eval Cases

### Case 1: Overly permissive IAM policy
```hcl
# BUGGY CODE — should be detected
resource "aws_iam_policy" "app_policy" {
  name = "app-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"  # All actions!
      Resource = "*"  # All resources!
    }]
  })
}
```
**Expected finding:** Critical — IAM policy grants all actions on all resources. Violates least-privilege principle. Restrict to specific actions (s3:GetObject) and resources (arn:aws:s3:::bucket/*).

### Case 2: Public S3 bucket
```hcl
# BUGGY CODE — should be detected
resource "aws_s3_bucket_acl" "docs" {
  bucket = aws_s3_bucket.docs.id
  acl    = "public-read" # Public!
}
```
**Expected finding:** High — S3 bucket ACL set to public-read. All objects publicly accessible. Use `private` ACL and CloudFront with OAI for public content.

### Case 3: Security group with SSH open to world
```hcl
# BUGGY CODE — should be detected
resource "aws_security_group" "web" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open to internet!
  }
}
```
**Expected finding:** High — SSH (port 22) open to 0.0.0.0/0. Allows brute-force attacks from internet. Restrict to VPN IP range or use AWS Systems Manager Session Manager.

## Counter-Examples

### Counter 1: Least-privilege IAM policy
```hcl
# CORRECT CODE — should NOT be flagged
resource "aws_iam_policy" "app_policy" {
  name = "app-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```
**Why it's correct:** IAM policy scoped to specific actions and resources.

### Counter 2: Private S3 with encryption
```hcl
# CORRECT CODE — should NOT be flagged
resource "aws_s3_bucket" "docs" {
  bucket = "my-docs"
}

resource "aws_s3_bucket_acl" "docs" {
  bucket = aws_s3_bucket.docs.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "docs" {
  bucket = aws_s3_bucket.docs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```
**Why it's correct:** Private ACL, encryption at rest enabled.

## Binary Eval Assertions
- [ ] Detects wildcard IAM in eval case 1
- [ ] Detects public S3 in eval case 2
- [ ] Detects open SSH in eval case 3
- [ ] Does NOT flag counter-example 1 (scoped IAM)
- [ ] Does NOT flag counter-example 2 (private + encrypted S3)
- [ ] Finding references OWASP IaC Security
- [ ] Severity assigned as high or critical
