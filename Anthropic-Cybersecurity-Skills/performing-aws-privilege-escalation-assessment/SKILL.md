---
name: performing-aws-privilege-escalation-assessment
description: "Perform authorized privilege escalation assessments in AWS environments. Signals: cloud privilege escalation, iam privilege escalation, container privilege escalation."
zh-signals: "Performing authorized privilege escalation assessments in AWS environments 信号:云提权,iam提权,容器提权。"
when-to-use: 'Performing authorized privilege escalation assessments in AWS environments
  to identify IAM misconfigurations that allow users or roles to elevate their permissions
  using Pacu, CloudFox, Principal Mapper, and manual IAM policy analysis techniques.

  '
domain: cybersecurity
subdomain: cloud-security
tags:
- cloud-security
- aws
- privilege-escalation
- iam
- pacu
- offensive-security
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

# Performing AWS Privilege Escalation Assessment

## When to Use

- When conducting authorized penetration testing of AWS IAM configurations
- When validating that IAM policies follow the principle of least privilege
- When assessing the blast radius of a compromised AWS credential
- When building security reviews for IAM role and policy changes in CI/CD pipelines
- When evaluating cross-account trust relationships for privilege escalation risks

**Do not use** for unauthorized testing against AWS accounts, for assessing non-IAM attack vectors (SSRF, application vulnerabilities), or as a substitute for comprehensive cloud penetration testing. Always obtain written authorization before testing.

## Prerequisites

- Written authorization for privilege escalation testing in the target AWS account
- Test IAM user or role with limited permissions as the starting point
- Pacu installed (`pip install pacu`)
- CloudFox installed (`go install github.com/BishopFox/cloudfox@latest`)
- PMapper (Principal Mapper) installed (`pip install principalmapper`)
- AWS CLI configured with test credentials and CloudTrail logging enabled for audit trail

## Workflow

### Step 1: Enumerate Starting Permissions

Establish the baseline permissions of the test principal before attempting escalation.

```bash
# Get current identity
aws sts get-caller-identity

# Enumerate inline and attached policies for the current user
aws iam list-user-policies --user-name test-user
aws iam list-attached-user-policies --user-name test-user

# Get group memberships and group policies
aws iam list-groups-for-user --user-name test-user
for group in $(aws iam list-groups-for-user --user-name test-user --query 'Groups[*].GroupName' --output text); do
  echo "=== Group: $group ==="
  aws iam list-group-policies --group-name "$group"
  aws iam list-attached-group-policies --group-name "$group"
done

# Simulate specific API calls to map effective permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT:user/test-user \
  --action-names iam:CreateUser iam:AttachUserPolicy iam:PassRole \
    lambda:CreateFunction ec2:RunInstances sts:AssumeRole \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' --output table
```

### Step 2: Scan for Privilege Escalation Paths with Pacu

Use Pacu's privilege escalation scanner to identify known IAM escalation techniques.

```bash
# Start Pacu session
pacu

# Create session and set credentials
Pacu (new:session) > set_keys --key-alias privesc-test

# Enumerate IAM configuration
Pacu > run iam__enum_users_roles_policies_groups
Pacu > run iam__enum_permissions

# Run privilege escalation scanner
Pacu > run iam__privesc_scan

# The scanner checks for 21+ known escalation methods including:
# - iam:CreatePolicyVersion (create admin policy version)
# - iam:SetDefaultPolicyVersion (revert to permissive older version)
# - iam:AttachUserPolicy / iam:AttachRolePolicy (attach admin policy)
# - iam:PutUserPolicy / iam:PutRolePolicy (create inline admin policy)
# - iam:PassRole + lambda:CreateFunction (Lambda with admin role)
# - iam:PassRole + ec2:RunInstances (EC2 with admin instance profile)
# - iam:CreateLoginProfile / iam:UpdateLoginProfile (set console password)
# - iam:CreateAccessKey (create keys for other users)
# - sts:AssumeRole (assume more privileged roles)
# - glue:CreateDevEndpoint + iam:PassRole (Glue with admin role)
```

### Step 3: Map Privilege Escalation Graphs with PMapper

Use Principal Mapper to build a graph of all IAM principals and identify escalation edges.

```bash
# Collect IAM data for graph construction
pmapper graph create --account ACCOUNT_ID

# Query for paths to admin
pmapper query 'who can do iam:AttachUserPolicy with * on *'
pmapper query 'who can do sts:AssumeRole with arn:aws:iam::ACCOUNT:role/AdminRole'

# Find all principals that can escalate to admin
pmapper analysis

# Visualize the privilege escalation graph
pmapper visualize --filetype png

# Check specific escalation paths
pmapper query 'can arn:aws:iam::ACCOUNT:user/test-user do iam:CreatePolicyVersion with *'
pmapper query 'can arn:aws:iam::ACCOUNT:user/test-user do sts:AssumeRole with arn:aws:iam::ACCOUNT:role/*'
```

### Step 4: Test Cross-Account Role Assumption

Evaluate cross-account trust policies for misconfigured role assumptions that allow unauthorized escalation.

```bash

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
