---
name: aws-iam-policy-analysis
description: "AWS IAM / resource policy analysis methodology. Use when the target involves AWS cloud services and provides IAM policies, resource policies, Lambda code, CloudFormation templates, or other policy files. Covers IAM policy dangerous pattern identification, resource policy Principal analysis, Condition key bypass patterns, and service trust relationship derivation. Use this skill when you find AWS policy files (json/yaml), *.amazonaws.com endpoints, or IAM ARNs"
zh-signals: "分析 AWS IAM 与资源策略文件，识别危险权限模式、Principal 暴露与 Condition 绕过以推导攻击面。信号:AWS策略分析,IAM权限,资源策略,Principal检查,条件绕过"
when-to-use: "Use when AWS IAM policies, resource policies, Lambda code, or CloudFormation templates are provided and you need to derive attack surface from the policy definitions."
metadata:
  tags: "aws,iam,policy,cloud,resource-policy,principal,condition,trust,policy analysis,permission analysis"
  category: "cloud"
---

# AWS IAM / Resource Policy Analysis Methodology

A systematic approach to analyzing AWS policy files (IAM policies, resource policies, Lambda code, etc.) once you have them. Core goal: **derive the attack surface from the policies instead of blindly enumerating**.

## ⛔ Further Reading (Must Read)

- S3 policy analysis + common vulnerability patterns → [references/s3-attack-techniques.md](references/s3-attack-techniques.md)
- Lambda/API Gateway/SNS resource policy vulnerability patterns → [references/aws-resource-policy-exploits.md](references/aws-resource-policy-exploits.md)

---

## Core Principles

1. **Policy files first** — when you get IAM policies / source code / CloudFormation templates, **analyze them first**, do not blindly enumerate
2. **Derive the attack surface from the policies** — policies tell you "what is allowed", and the attack surface lies at "the boundary of what is allowed"
3. **Principal is the entry point** — `"Principal": "*"` means cross-account/anonymous access and is the highest-priority check
4. **Conditions can be bypassed** — `StringLike` wildcards mean different things in different protocols/contexts
5. **Trust relationships > individual permissions** — focus on the trust chains between services (who can call whom, who can pass roles to whom)

---

## Step 1: Quick Classification of Policy Files

After obtaining attached or downloaded files, classify them first:

| File type | How to recognize | Focus |
|---------|---------|--------|
| IAM Policy | `"Version": "2012-10-17"`, `"Statement"` | Action/Resource scope |
| Resource Policy | same as above, but with a `Principal` field | Who can access, condition restrictions |
| Lambda code | `.py`/`.js` files, `handler(event, context)` | Input handling, path concatenation, injection points |
| CloudFormation | `AWSTemplateFormatVersion`, `Resources` | Full architecture, role bindings |
| Trust Policy | `"Action": "sts:AssumeRole"` | Who can assume the role |

---

## Step 2: IAM Policy Dangerous Pattern Identification

### 2.1 Check the Principal

```
🔴 "Principal": "*"              → any AWS identity (including anonymous) can access
🔴 "Principal": {"AWS": "*"}     → same as above
🟡 "Principal": {"Service": "lambda.amazonaws.com"}  → a specific service can invoke it
🟢 "Principal": {"AWS": "arn:aws:iam::123456:root"}  → restricted to one account
```

### 2.2 Check the Action Scope

| Action pattern | Risk |
|------------|------|
| `"Action": "*"` | 🔴 Full control |
| `"Action": "s3:*"` | 🔴 Full control of S3 |
| `"Action": ["s3:GetObject", "s3:PutObject"]` | 🟡 Readable and writable |
| `"Action": "s3:GetObject"` on `"Resource": "*"` | 🟡 Readable for every bucket |
| `"Action": "sts:AssumeRole"` | 🟡 Can switch roles (privilege escalation entry point) |
| `"Action": "iam:PassRole"` | 🟡 Can pass roles (indirect privilege escalation) |
| `"Action": "lambda:InvokeFunction"` with `Principal:*` | 🔴 Anyone can invoke the Lambda |

### 2.3 Check the Resource Scope

```
🔴 "Resource": "*"                          → all resources
🟡 "Resource": "arn:aws:s3:::bucket/*"      → all objects in the bucket
🟢 "Resource": "arn:aws:s3:::bucket/public/*" → only the public prefix
```

### 2.4 Check for Condition Bypasses

```json
// StringLike wildcard — means different things in different contexts
"Condition": {"StringLike": {"sns:Endpoint": "*@company.com"}}
// email protocol: Endpoint = mailbox → must be xxx@company.com
// https protocol: Endpoint = URL → any URL containing @company.com bypasses it

// IpAddress condition — may be bypassed via VPN/proxy
"Condition": {"IpAddress": {"aws:SourceIp": "10.0.0.0/8"}}

// StringEquals vs StringLike — the former matches exactly, the latter supports wildcards
```

---

## Step 3: Deriving the Service Trust Relationship Graph

Draw the "who trusts whom" call relationships from the policy files:

```
Read all policy files
    ↓
Identify all Principals (who the callers are)
    ↓
Identify all Resources (what is accessed)
    ↓
Connect the lines: Principal → Action → Resource
    ↓
Find the weakest link (Principal:* or an edge with overly broad permissions)
```

Common service relationships:
- API Gateway → Lambda (the API GW triggers the Lambda)
- Lambda → S3/DynamoDB/SNS (Lambda execution role permissions)
- SNS → Lambda/SQS/HTTP (message push targets)
- IAM User → AssumeRole → high-privilege role

**Key**: analyze the permissions of the Lambda execution role — it determines what resources the Lambda can access.

---

## Step 4: Lambda / Application Code Audit

After obtaining the Lambda code (handler.py/index.js), focus on:

| Vulnerability type | Code pattern | Exploitation |
|---------|---------|---------|
| Path traversal | `os.path.join(prefix, user_input)` | Absolute path bypass: `/flag` |
| Command injection | `os.system(f"cmd {user_input}")` | `; cat /flag` |
| SSRF | `requests.get(user_input)` | `http://169.254.169.254/...` |
| Environment variable leak | `os.environ['SECRET']` | Error message/stack trace |
| SQL injection | string-concatenated SQL | `' OR 1=1 --` |
| Deserialization | `pickle.loads()`/`yaml.load()` | Craft a malicious object |

---

## Step 5: AWS Service Endpoint Discovery

```bash
# Extract AWS related URLs from the target page
curl -s TARGET_URL | grep -oE 'https?://[a-z0-9.-]+\.amazonaws\.com[^"]*'
curl -s TARGET_URL | grep -oE 'https?://[a-z0-9]+\.execute-api\.[a-z0-9-]+\.amazonaws\.com[^"]*'

# Extract S3 bucket and API GW URLs from JS/HTML
curl -s TARGET_URL | grep -oE 's3\.amazonaws\.com/[^"]*'

# Presigned URL information leak
# X-Amz-Credential contains the AccessKeyId and the Region
```

---

## Step 6: Common Helper Tools

```bash
# webhook.site — receive AWS service callbacks (SNS, S3 Events, etc.)
# Use it when you need an external endpoint to receive AWS pushes

# AWS CLI policy inspection
aws iam get-policy-version --policy-arn ARN --version-id v1
aws s3api get-bucket-policy --bucket BUCKET
aws lambda get-policy --function-name FUNC

# ScoutSuite — AWS security configuration audit
# Prowler — AWS security baseline checks
```

---

## ⚠️ Mistakes to Avoid

1. **Do not blindly enumerate** — after 3 consecutive AccessDenied/404 responses, stop and re-analyze the policies
2. **Do not ignore attachments** — the policy files in the attachments contain all the information needed to solve the task
3. **Do not assume a fixed attack chain** — every scenario has a different combination of services and vulnerability points, so start from the policy analysis instead of applying a template
4. **Do not ignore the Condition field** — many seemingly safe policies have a Condition that can be bypassed
