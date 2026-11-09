---
name: conducting-cloud-penetration-testing
description: "Outline methodologies for authorized penetration testing. Signals: pwn, binary exploitation, stack overflow."
zh-signals: "This skill outlines methodologies for performing authorized penetration 信号:pwn,二进制利用,栈溢出。"
when-to-use: 'This skill outlines methodologies for performing authorized penetration
  testing against AWS, Azure, and GCP cloud environments. It covers understanding
  the shared responsibility model for testing scope, leveraging cloud-specific attack
  tools like Pacu and ScoutSuite, exploiting IAM misconfigurations, testing for SSRF
  to cloud metadata services, and reporting findings aligned to MITRE ATT&CK Cloud
  matrix.

  '
domain: cybersecurity
subdomain: cloud-security
tags:
- cloud-pentesting
- offensive-security
- aws-exploitation
- shared-responsibility
- mitre-attack-cloud
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
d3fend_techniques:
- Token Binding
- Restore Access
- Application Protocol Command Analysis
- Reissue Credential
- Network Isolation
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
mitre_attack:
- T1078.004
- T1580
- T1530
- T1538
---

# Conducting Cloud Penetration Testing

## When to Use

- When performing authorized security assessments of cloud environments before production deployment
- When validating cloud security controls after a major architectural change or migration
- When compliance requirements mandate annual penetration testing of cloud infrastructure
- When testing incident response readiness by simulating realistic cloud-based attack scenarios
- When assessing lateral movement risk across multi-account or multi-cloud environments

**Do not use** for unauthorized testing against cloud accounts, for testing cloud provider infrastructure itself (covered by the shared responsibility model), or for DDoS simulation without explicit cloud provider approval.

## Prerequisites

- Written authorization from the cloud account owner and scope definition document
- AWS, Azure, or GCP penetration testing policy acknowledgment (AWS no longer requires pre-approval for most services)
- Isolated testing account or explicitly scoped production account with breakglass procedures
- Cloud-specific offensive tooling installed: Pacu (AWS), ScoutSuite, Prowler, CloudFox
- MITRE ATT&CK Cloud matrix for finding classification

## Workflow

### Step 1: Define Scope and Rules of Engagement

Establish testing boundaries based on the shared responsibility model. The customer is responsible for testing configurations, IAM policies, application security, and data protection. The cloud provider manages physical infrastructure, hypervisor, and managed service internals.

```
Cloud Penetration Test Scope Document
=======================================
Target: AWS Account 123456789012 (Production)
Testing Window: 2025-02-24 08:00 UTC to 2025-02-28 18:00 UTC
Authorization: Signed by CISO, dated 2025-02-20

IN SCOPE:
  - IAM users, roles, policies, and cross-account trust
  - EC2 instances, security groups, and network ACLs
  - S3 bucket policies and data access controls
  - Lambda functions, API Gateway endpoints
  - RDS/DynamoDB access controls and encryption
  - EKS cluster RBAC and network policies
  - CloudTrail, Config, and monitoring gaps

OUT OF SCOPE:
  - AWS managed service internals (RDS engine, Lambda runtime)
  - DDoS attacks or volumetric testing
  - Physical infrastructure or hypervisor attacks
  - Social engineering of AWS support

EMERGENCY CONTACT: security-ops@company.com, +1-555-0199
```

### Step 2: Reconnaissance and Cloud Enumeration

Use cloud-specific tools to enumerate the attack surface: exposed services, public IPs, S3 buckets, IAM configurations, and metadata endpoints.

```bash
# ScoutSuite multi-cloud assessment
scout suite aws --profile target-account --report-dir ./scout-report

# Prowler comprehensive AWS security assessment
prowler aws -M json-ocsf -o ./prowler-output --profile target-account

# CloudFox for identifying privilege escalation paths
cloudfox aws --profile target-account all-checks

# Enumerate public S3 buckets
for bucket in $(aws s3api list-buckets --query 'Buckets[*].Name' --output text); do
  aws s3api get-bucket-policy-status --bucket $bucket 2>/dev/null | grep -q "true" && echo "PUBLIC: $bucket"
done

# Check for IMDS v1 (vulnerable to SSRF)
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,MetadataOptions.HttpTokens]' \
  --output table
```

### Step 3: IAM Privilege Escalation Testing

Use Pacu to identify and exploit IAM misconfigurations that allow privilege escalation from a low-privilege starting point to administrative access.

```bash
# Initialize Pacu session
pacu

# Set stolen or test credentials
set_keys --key-alias test-creds

# Run IAM enumeration modules
run iam__enum_users_roles_policies_groups
run iam__enum_permissions

# Check for privilege escalation paths
run iam__privesc_scan

# Common escalation paths to test:
# 1. iam:CreatePolicyVersion - Create new policy version with admin access
# 2. iam:AttachUserPolicy - Attach AdministratorAccess to self
# 3. iam:PassRole + lambda:CreateFunction - Create Lambda with admin role
# 4. iam:PassRole + ec2:RunInstances - Launch EC2 with admin instance profile

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
