---
name: cloud-iam-audit
description: "Cloud IAM permission auditing and privilege escalation. Use when you have obtained cloud platform credentials (AWS AK/SK, Azure SPN, GCP SA, Tencent Cloud SecretId/SecretKey) and need to assess the permission scope and escalation paths. Covers IAM/CAM policy analysis for AWS/Azure/GCP/Tencent Cloud, common escalation paths (PassRole, AssumeRole, Lambda/SCF escalation), cross-account attacks, and CloudTrail/CloudAudit evasion. Use this skill whenever any cloud credential, AK/SK, SecretId/SecretKey is found"
zh-signals: "审计 AWS/Azure/GCP/腾讯云凭据的权限范围与提权路径。信号:云IAM,提权,AWS,Azure,腾讯云,PassRole"
when-to-use: "Use when you obtain cloud credentials such as AWS AK/SK, Azure SPN, GCP SA keys, or Tencent Cloud keys and must assess permissions and escalation paths."
metadata:
  tags: "cloud,iam,cam,audit,privilege,escalation,aws,azure,gcp,tencent,tencentcloud,escalation,permission,credential,PassRole,SecretId"
  category: "cloud"
---

# Cloud IAM Permission Audit and Privilege Escalation Methodology

IAM/CAM permissions are the attack surface — an over-permissive policy is more dangerous than an RCE vulnerability.

## ⛔ Further Reading (Must Read)

- Detailed commands for the 5 AWS escalation paths, high-value data searches, and CloudTrail stealth → [references/aws-escalation.md](references/aws-escalation.md)
- Tencent Cloud CAM escalation paths, tccli/SDK commands, and CloudAudit stealth → [references/tencent-cam-escalation.md](references/tencent-cam-escalation.md)

---

## Phase 1: Credential Identification and Identity Confirmation

| Credential | Format | Source |
|------|------|------|
| AWS AK/SK | `AKIA...` (20 characters) | Configuration file, environment variable, metadata |
| AWS temporary credentials | `ASIA...` + SessionToken | IMDS, STS AssumeRole |
| Azure SPN | client_id + client_secret + tenant_id | Configuration file |
| GCP SA key | JSON file containing `private_key` | Service account key file |
| Tencent Cloud SecretId/SecretKey | `AKIDz...` (36 characters) / `xxx=` (Base64) | Configuration file, environment variable, metadata |
| Tencent Cloud temporary credentials | SecretId/SecretKey + Token/ExpiredTime | Metadata, STS AssumeRole |

```bash
# AWS: who am I
aws sts get-caller-identity

# Azure
az account show

# GCP
gcloud auth list

# Tencent Cloud: who am I (prefer tccli)
tccli sts GetCallerIdentity
# Or use the SDK
python3 -c "
from tencentcloud.sts.v20180813 import sts_client, models
from tencentcloud.common import credential
cred = credential.Credential('SecretId', 'SecretKey')
client = sts_client.StsClient(cred, 'ap-guangzhou')
print(client.GetCallerIdentity(models.GetCallerIdentityRequest()).to_json_string())
"
```

### Tencent Cloud Credential Configuration

```bash
# Interactive tccli configuration (preferred)
tccli configure
# Enter: SecretId, SecretKey, Region (e.g. ap-guangzhou), Output (json)

# When using temporary credentials, set the Token additionally
tccli configure set token "TOKEN_VALUE"

# It can also be set through environment variables
export TENCENTCLOUD_SECRET_ID="AKIDz..."
export TENCENTCLOUD_SECRET_KEY="xxxx="
export TENCENTCLOUD_SESSION_TOKEN="TOKEN"  # for temporary credentials
```

---

## Phase 2: Permission Enumeration

### AWS Permission Enumeration
```bash
aws iam list-attached-user-policies --user-name <user>
aws iam list-attached-role-policies --role-name <role>
# Brute-force enumeration
aws s3 ls 2>&1; aws ec2 describe-instances 2>&1; aws iam list-users 2>&1
```

### Tencent Cloud CAM Permission Enumeration (prefer tccli)

```bash
# 1. Account overview
tccli cam GetAccountSummary

# 2. List sub-users
tccli cam ListUsers

# 3. List user groups
tccli cam ListGroups --Page 1 --Rp 50

# 4. List roles (critical — roles can be abused through AssumeRole)
tccli cam DescribeRoleList --Page 1 --Rp 50

# 5. List policies (custom policies are the key to privilege escalation)
tccli cam ListPolicies --Scope Local --Page 1 --Rp 100   # custom policies only
tccli cam ListPolicies --Scope All --Page 1 --Rp 100      # all policies

# 6. View the content of a specific policy
tccli cam GetPolicy --PolicyId <PolicyId> --PolicyVersion 1

# 7. View the policies attached to a user
tccli cam ListAttachedUserPolicies --TargetUin <UIN>

# 8. View the policies attached to a role
tccli cam ListAttachedRolePolicies --RoleId <RoleId>

# 9. View the policies attached to a user group
tccli cam ListAttachedGroupPolicies --GroupId <GroupId>

# 10. List a user's AccessKeys
tccli cam ListAccessKeys

# 11. View role details (includes the trust policy — key for cross-account attacks)
tccli cam GetRole --RoleId <RoleId>

# 12. View the groups a user belongs to
tccli cam ListGroupsForUser --Uin <UIN>
```

### Tencent Cloud Brute-Force Enumeration (probe service by service)

```bash
# COS storage (tccli cos does not support GetService, use the SDK or coscli)
coscli ls 2>&1
# Or the Python SDK:
# pip install cos-python-sdk-v5
# from qcloud_cos import CosConfig, CosS3Client
# client = CosS3Client(CosConfig(Region='ap-guangzhou', SecretId='Sid', SecretKey='Skey'))
# print(client.list_buckets())

# CVM instances
tccli cvm DescribeInstances 2>&1

# SCF cloud functions (similar to the Lambda escalation path)
tccli scf ListFunctions --Namespace default --Limit 50 2>&1

# CBS cloud disks
tccli cbs DescribeDisks 2>&1

# SSL certificates (may contain private keys)
tccli ssl DescribeCertificates --Limit 50 2>&1

# TDSQL/MySQL
tccli cdb DescribeDBInstances 2>&1

# Key management (KMS)
tccli kms ListKeys --Limit 50 2>&1
```

### Permission Level Quick Reference
| Achievable Operations | Escalation Potential |
|------------|----------|
| GetCallerIdentity only | Low |
| cos:GetObject / s3:GetObject | Medium (may find more credentials) |
| cam:List*, cam:Get* / iam:List*, iam:Get* | Medium (enables analysis of escalation paths) |
| cam:CreateUser/AttachUserPolicy | **High** (direct privilege escalation) |
| cam:CreateRole/AttachRolePolicy | **High** (create a high-privilege role) |
| cam:PassRole + scf:CreateFunction | **High** (indirect privilege escalation — attach a high-privilege role to SCF) |
| sts:AssumeRole | **High** (hop to a higher-privilege role) |

---

## Phase 3: Privilege Escalation Decision Tree

```
Current privileges?
├─ Can manipulate IAM/CAM (CreatePolicy/AttachPolicy) → direct privilege escalation
├─ Has PassRole + Lambda/SCF → indirect privilege escalation (create a service bound to a high-privilege role)
├─ Has AssumeRole → role chain hopping
├─ Data read access only → find more credentials (COS/S3/Secrets/Lambda/SCF code/User-Data)
└─ Detailed commands
    ├─ AWS → [references/aws-escalation.md](references/aws-escalation.md)
    └─ Tencent Cloud → [references/tencent-cam-escalation.md](references/tencent-cam-escalation.md)
```

## Notes
- The core of cloud privilege escalation: you must be able to manipulate **IAM/CAM itself** to escalate
- Temporary credentials expire, so prefer long-lived AK/SK or create a backdoor Access Key
- The cross-account trust policy is a critical audit point
- The Tencent Cloud role trust policy uses the `qcs::cam::uin/ROOT_UIN:uin/ANY_UIN` format
- Tencent Cloud policy syntax resembles AWS but uses the `qcs` resource descriptor
- Operations generate CloudTrail/CloudAudit logs — watch your operational traces

## Escalation Path Overview
- **Direct privilege escalation**: create a policy that grants yourself `*:*` permissions
- **Indirect privilege escalation**: PassRole + SCF/Lambda creates a function bound to a high-privilege role
- **Role chain**: current identity → AssumeRole → higher-privilege role
- **Permission enumeration tools**: enumerate-iam, Pacu (AWS); custom scripts (Tencent Cloud)
