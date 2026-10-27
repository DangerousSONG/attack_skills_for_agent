---
name: performing-cloud-penetration-testing-with-pacu
description: "Run authorized AWS penetration tests with Pacu, the open-source AWS exploitation 信号:pwn,二进制利用,栈溢出。"
when-to-use: 'Run authorized AWS penetration tests with Pacu, the open-source AWS exploitation
  framework, to enumerate IAM configuration, scan for privilege escalation paths, and
  test data access and lateral movement using compromised credentials. Use when conducting
  authorized red-team assessments of AWS environments, validating IAM policies and
  SCPs, or determining the blast radius of compromised AWS credentials.

  '
domain: cybersecurity
subdomain: cloud-security
tags:
- cloud-security
- aws
- pacu
- penetration-testing
- offensive-security
- iam-exploitation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
mitre_attack:
- T1078.004
- T1530
- T1537
- T1580
- T1068
---

# Performing Cloud Penetration Testing with Pacu

## When to Use

- When conducting authorized penetration testing of AWS environments
- When validating the effectiveness of IAM policies, SCPs, and permission boundaries
- When assessing the blast radius of a compromised set of AWS credentials
- When testing detection capabilities of GuardDuty, Security Hub, and custom alerting
- When building red team exercises against AWS cloud infrastructure

**Do not use** for unauthorized testing of any AWS account, for testing AWS infrastructure itself (covered by shared responsibility), for DDoS or volumetric attacks without AWS approval, or for production account testing without explicit authorization and breakglass procedures.

## Prerequisites

- Written authorization from the AWS account owner with defined scope and rules of engagement
- Pacu v1.5+ installed (`pip install pacu`)
- Test AWS credentials with limited starting permissions (simulates compromised credential scenario)
- CloudTrail logging enabled to capture all Pacu activity for post-engagement review
- GuardDuty enabled to validate detection of Pacu activities
- Emergency contact and rollback procedures documented

## Workflow

### Step 1: Initialize Pacu Session and Configure Credentials

Set up a Pacu session with the test credentials and define the engagement scope.

```bash
# Install Pacu
pip install pacu

# Start Pacu
pacu

# Create a new session for the engagement
Pacu > set_keys --key-alias pentest-target
# Enter Access Key ID: AKIA...
# Enter Secret Access Key: ...

# Verify identity
Pacu > whoami

# Review available modules
Pacu > list
Pacu > search iam
Pacu > search ec2
Pacu > search s3
```

### Step 2: Enumerate IAM Configuration

Run IAM enumeration modules to map users, roles, policies, and group memberships.

```bash
# Comprehensive IAM enumeration
Pacu > run iam__enum_users_roles_policies_groups

# Enumerate detailed permissions for the current principal
Pacu > run iam__enum_permissions

# Enumerate account authorization details (requires iam:GetAccountAuthorizationDetails)
Pacu > run iam__get_credential_report

# Enumerate role trust policies for cross-account access
Pacu > run iam__enum_roles

# Check current session data
Pacu > data iam
```

### Step 3: Scan for Privilege Escalation Paths

Use Pacu's privilege escalation scanner to identify all exploitable escalation vectors.

```bash
# Run the privilege escalation scanner
Pacu > run iam__privesc_scan

# The scanner tests for 21+ escalation methods:
# Method 1:  iam:CreatePolicyVersion
# Method 2:  iam:SetDefaultPolicyVersion
# Method 3:  iam:PassRole + ec2:RunInstances
# Method 4:  iam:PassRole + lambda:CreateFunction + lambda:InvokeFunction
# Method 5:  iam:PassRole + lambda:CreateFunction + lambda:CreateEventSourceMapping
# Method 6:  iam:PassRole + glue:CreateDevEndpoint
# Method 7:  iam:PassRole + cloudformation:CreateStack
# Method 8:  iam:PassRole + datapipeline:CreatePipeline
# Method 9:  iam:CreateAccessKey
# Method 10: iam:CreateLoginProfile
# Method 11: iam:UpdateLoginProfile
# Method 12: iam:AttachUserPolicy
# Method 13: iam:AttachGroupPolicy
# Method 14: iam:AttachRolePolicy
# Method 15: iam:PutUserPolicy
# Method 16: iam:PutGroupPolicy
# Method 17: iam:PutRolePolicy
# Method 18: iam:AddUserToGroup
# Method 19: iam:UpdateAssumeRolePolicy
# Method 20: sts:AssumeRole
# Method 21: lambda:UpdateFunctionCode

# If escalation paths found, attempt exploitation
Pacu > run iam__privesc_scan --escalate
```

### Step 4: Enumerate and Test Data Access

Discover accessible data stores including S3, DynamoDB, RDS, and Secrets Manager.

```bash
# Enumerate S3 buckets
Pacu > run s3__bucket_finder

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
