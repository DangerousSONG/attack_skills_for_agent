---
name: cicd-pipeline-attack
description: "CI/CD pipeline and supply chain attack methodology. Use when you discover that a target uses GitHub Actions, Jenkins, GitLab CI, CircleCI, Terraform Cloud, Atlantis or another CI/CD system, when you need to test pipeline security, or when you find configuration files such as .github/workflows, Jenkinsfile, or .gitlab-ci.yml. Covers the three PPE (Poisoned Pipeline Execution) attack modes (D-PPE/I-PPE/3PE), the VCS attack surface (code leak, webhook abuse, branch protection bypass), Pipeline Secrets theft and lateral movement, and the paths from CI/CD into cloud environments."
zh-signals: "针对 GitHub Actions、Jenkins、GitLab CI 等 CI/CD 流水线与供应链的 PPE/Secrets 攻击方法。信号:CI/CD攻击,PPE,供应链,GitHub Actions,Jenkins,Secrets窃取"
when-to-use: "Use when a target uses GitHub Actions, Jenkins, GitLab CI, CircleCI, Terraform Cloud, or Atlantis, or when CI/CD config files are discovered."
metadata:
  tags: "cicd,pipeline,github-actions,jenkins,gitlab,terraform,atlantis,supply-chain,PPE,poisoned-pipeline,secrets,VCS,webhook"
  category: "cloud"
---

# CI/CD Pipeline and Supply Chain Attack Methodology

CI/CD systems are core infrastructure for modern software engineering — they hold read/write access to code repositories, carry cloud platform deployment credentials, and can modify production environments directly. Once a pipeline is compromised, the attacker gains code control, Secrets access, and cloud environment penetration at the same time, and the blast radius far exceeds the compromise of a single server.

This skill organizes the CI/CD attack methodology as a decision tree. For detailed techniques on each platform, see the corresponding reference documents.

## Further Reading

Once you have identified the concrete platform, load the matching reference document for full attack details:

- GitHub Actions specific attack techniques → read [references/github-actions-abuse.md](references/github-actions-abuse.md)
- Jenkins / Terraform / Atlantis / GitLab CI / Azure DevOps / CircleCI / Drone / Buildkite and other platforms → read [references/platform-specific.md](references/platform-specific.md)
- Cross-platform build file injection (package.json, setup.py, Makefile, Bazel, Maven/Gradle, csproj) → read [references/build-file-injection.md](references/build-file-injection.md)

## Phase 0: CI/CD System Identification

You can determine the CI/CD platform by finding the following marker files in the target repository or infrastructure:

| Marker file / characteristic | CI/CD platform | Next step |
|---|---|---|
| `.github/workflows/*.yml` | GitHub Actions | → Phase 2 PPE + see github-actions-abuse.md |
| `Jenkinsfile` or the `/script` console | Jenkins | → Phase 4 Jenkins specifics + see platform-specific.md |
| `.gitlab-ci.yml` | GitLab CI | → Phase 2 PPE + see platform-specific.md |
| `.circleci/config.yml` | CircleCI | → Phase 2 PPE + see platform-specific.md |
| `azure-pipelines.yml` | Azure DevOps | → Phase 2 PPE + service connection Secret extraction |
| `.drone.yml` | Drone CI | → Phase 2 PPE + self-hosted Runner check |
| `.buildkite/*.yml` | Buildkite | → Phase 2 PPE + Agent cloud/K8s permission check |
| `atlantis.yaml` + Webhook | Atlantis | → Phase 4 Atlantis specifics |
| `*.tf` + Terraform Cloud | Terraform Cloud | → Phase 4 Terraform specifics |
| `serverless.yml` | Serverless Framework | → see platform-specific.md |
| `docker-compose.yml` + CI trigger | Docker Build | → Check for build context leakage |
| Airflow DAGs / Concourse pipeline | Airflow / Concourse | → see platform-specific.md |

**Quick identification tips**:
- After cloning the repository, search for the configuration files: look for `Jenkinsfile`, `.github/workflows`, `.gitlab-ci.yml`, `.circleci`, `atlantis.yaml`
- Inspect the webhook configuration: webhook URLs expose the CI/CD service type and internal addresses
- Enumerate CI/CD service ports: Jenkins defaults to 8080, Atlantis to 4141, GitLab Runner to 8093

## Phase 1: VCS Attack Surface

Before moving into pipeline attacks, the VCS (version control system) is itself an important attack surface.

### 1.1 Code Leakage

Common sources of sensitive information in code repositories:

- **Git history**: deleted keys/credentials may still live in the commit history (`git log -p` across all branches)
- **Public repositories**: use GitHub Dorks to search organization names + keywords (`password`, `secret`, `token`, `AWS_`)
- **Deleted fork data**: commit data from forks deleted on GitHub can still be reached through the commit hash
- **Exposed internal repositories**: fork data from before a private repository became public can be brute-forced with short SHA-1 values

### 1.2 Branch Protection Bypass

Branch protection is the key defense against merging malicious code, but there are multiple bypass routes:

| Bypass scenario | Condition | Attack method |
|---|---|---|
| Insufficient approvals | Control multiple accounts | Use another account to approve your own PR |
| GITHUB_TOKEN self-approval | Actions has write permission | Approve the PR through GITHUB_TOKEN in Actions |
| Approval not invalidated after push | "dismiss on push" not enabled | First submit legitimate code to get approval, then push malicious code |
| Misconfigured CODEOWNERS | The file format is wrong | GitHub raises no error but CODEOWNERS protection is ineffective |
| New branches unprotected | Wildcard `*` is used but with a delay | When a new branch is created the branch protection has not taken effect yet, so the first push can trigger Actions |
| Admin exemption | Admins are not covered by the rules | Admins can bypass all branch protection directly |
| PR hijacking | You can modify someone else's PR | Inject malicious code into someone else's PR and then approve and merge it yourself |

### 1.3 Webhook Abuse

- **No Secret validation**: the attacker can forge webhook requests to trigger pipelines
- **Secret exposed in the URL**: the Secret is attached as a URL parameter and is easily logged
- **IP allowlist bypass**: create an account on GitHub/GitLab and configure a webhook to send requests to allowlisted Jenkins/Atlantis instances
- **Bitbucket Cloud**: does not support webhook Secrets, so it can only rely on IP allowlists

## Phase 2: PPE -- Poisoned Pipeline Execution

PPE is the core framework for CI/CD attacks. The attacker "poisons" the pipeline by modifying the CI configuration file or a file it depends on, so that it executes malicious commands.

### PPE Determination Decision Tree

```
Can you write to / modify the CI configuration file (workflow yml / Jenkinsfile / .gitlab-ci.yml)?
├── Yes → D-PPE (direct poisoning)
│   ├── Can you push directly to the triggering branch → simplest path
│   └── A PR is required → check whether the PR triggers the pipeline
│
├── No, but can you modify a file the CI configuration depends on?
│   ├── Makefile / build.sh / package.json / requirements.txt → I-PPE (indirect poisoning)
│   ├── Terraform .tf files → I-PPE via external data source
│   └── Dockerfile → I-PPE via build context
│
└── No, and no repository write permission?
    └── 3PE (third-party poisoning)
        ├── Can you submit an external PR? → pull_request trigger
        ├── Is the PR title/description injected into a shell command? → Context Script Injection
        └── Can you trigger it through an issue/comment? → issue_comment trigger
```

### D-PPE (Direct PPE)

The attacker directly modifies the CI configuration file. This is the most direct attack path:

- **Prerequisite**: repository write permission, or the ability to trigger a pipeline that uses the PR branch configuration through a PR
- **Target files**: `.github/workflows/*.yml`, `Jenkinsfile`, `.gitlab-ci.yml`, `.circleci/config.yml`
- **Key condition**: some platforms (such as the GitHub Actions `pull_request` trigger) use the workflow version from the PR submitter — this means the attacker's modifications get executed

### I-PPE (Indirect PPE)

The attacker does not modify the CI configuration file itself, but modifies the files the CI configuration depends on:

- **Build scripts**: `Makefile`, `build.sh`, the `scripts` field of `package.json`
- **Dependency files**: `requirements.txt`, `package-lock.json` (supply chain injection)
- **IaC configuration**: `external` data sources or `local-exec` provisioners in Terraform `.tf` files
- **Docker builds**: control the Dockerfile or the build context path

The limitation of I-PPE is that the attacker can only access the Secrets the pipeline already loads, and cannot declare new Secret references through configuration.

### 3PE (Third-Party PPE / Public PPE)

External attackers without repository write permission trigger the pipeline in the following ways:

**Context Script Injection (most common):**

When the CI configuration uses user-controllable expressions such as `${{ github.event.pull_request.title }}` to build shell commands in a `run:` step, the attacker can inject commands through the PR title. GitHub Actions renders the expression before execution, so shell quoting escapes cannot defend against it.

**Comparison of dangerous triggers:**

| Trigger | Secrets access | Write permission | Code version used | Risk |
|---|---|---|---|---|
| `pull_request` | None (GITHUB_TOKEN is read-only) | None | PR branch | Low (but malicious Artifacts can be uploaded) |
| `pull_request_target` | Yes | Yes | Base branch (safe by default) | High (extremely dangerous if the PR code is checked out) |
| `workflow_run` | Yes | Yes | Depends on the configuration | High (often chained for exploitation) |
| `issue_comment` | Yes | Yes | Base branch | High (RCE when combined with checking out the PR ref) |

**The fatal misuse of `pull_request_target`:**

Although `pull_request_target` runs in the base branch context (which looks safe), if the workflow explicitly checks out the PR code (`ref: ${{ github.event.pull_request.head.sha }}`), the attacker's code executes in an environment that holds Secrets and write permission.

## Phase 3: Secrets Theft and Lateral Movement

After successfully poisoning the pipeline, the core goal is to steal Secrets and expand outward.

### 3.1 Secrets Extraction Methods

**Environment variables:**
- `env | base64` exports all environment variables (base64 encoding bypasses GitHub's log masking)
- Double base64 encoding further bypasses masking: `echo '${{ toJson(secrets) }}' | base64 -w0 | base64 -w0`

**Filesystem:**
- Temporary script files: `/home/runner/work/_temp/*` (GitHub Actions stores the rendered scripts there)
- Process memory: use `gcore` or `/proc/<pid>/mem` to read plaintext Secrets from the Runner.Worker/Runner.Listener processes

**When direct exfiltration is impossible:**
- Use GITHUB_TOKEN to create a repository/issue/comment as a data relay
- Write the Secrets into an Artifact upload
- Write into the Actions log (mind the masking rules)

### 3.2 Pivoting from CI/CD into the Cloud Environment

CI/CD Runners usually hold cloud platform credentials for deployment. These credentials are the bridge from CI/CD into the cloud environment:

| Credential source | Location | Exploitation method |
|---|---|---|
| OIDC Token (GitHub → AWS/GCP/Azure) | `id-token: write` permission | Request an OIDC Token → AssumeRoleWithWebIdentity |
| AWS static AK/SK | Environment variables or Secrets | Refer to the `cloud-aksk-exploit` skill |
| GCP Service Account JSON | File or environment variables | Refer to the `gcp-pentesting` skill |
| Azure Service Principal | Environment variables | Refer to the Azure content in the `aws-pentesting` skill |
| Terraform Cloud Runner credentials | `tfc-aws-*`/`tfc-gcp-*` files | Use the CLI directly to operate on cloud resources |
| Kubernetes kubeconfig | `~/.kube/config` or a mounted SA Token | Cluster takeover |
| Docker Registry Token | `~/.docker/config.json` | Push a malicious image |

**Additional attack surface of self-hosted Runners:**
- Cloud metadata service (169.254.169.254) → obtain the IAM role credentials bound to the instance
- Lateral movement inside the internal network → reach other services in the internal network
- Docker API (2375/tcp) → container escape
- Kubernetes cluster access → DaemonSet lateral expansion

### 3.3 Production Takeover

If the pipeline is directly responsible for production deployment:

- **Code tampering**: inject backdoor code into the build artifacts
- **Supply chain attack**: tamper with the npm/PyPI package publishing flow (steal the publish token → publish a malicious version)
- **Image poisoning**: modify the Docker image layers to inject malicious code
- **IaC tampering**: modify the Terraform/CloudFormation configuration to create backdoor resources

## Phase 4: Platform-Specific Attacks

### 4.1 GitHub Actions

GitHub Actions is one of the most widely used CI/CD platforms and has a rich attack surface:

- **Artifact Poisoning**: a low-privilege workflow uploads a malicious Artifact → a high-privilege workflow downloads and executes it
- **Cache Poisoning**: caches shared across workflows have no trust isolation → poison scripts/binaries in the cache
- **GITHUB_TOKEN abuse**: merge PRs, approve PRs, create PRs
- **Action tag hijacking**: after obtaining write permission on an Action repository, force-push a tag to point at a malicious commit
- **AI Agent injection**: LLM Agents in CI (Gemini/Claude Code Action) can be controlled through prompt injection

→ read [references/github-actions-abuse.md](references/github-actions-abuse.md)

### 4.2 Jenkins

Jenkins's high-privilege characteristics make it a high-value target:

- **Groovy Script Console** (`/script`) → direct RCE
- **Pipeline creation/modification** → execute arbitrary commands through a Jenkinsfile
- **Credential dump** → use a Groovy script to export every key in credentials.xml
- **File read → RCE** → read `master.key` + `hudson.util.Secret` → decrypt all credentials offline → forge the remember-me Cookie

→ read [references/platform-specific.md](references/platform-specific.md)

### 4.3 Terraform / Atlantis

The core of attacks against IaC tools is that code is execution:

- **Terraform Plan RCE**: an `external` data source or a malicious Provider can execute code during the `plan` phase
- **Terraform Apply RCE**: a `local-exec` provisioner executes during the `apply` phase
- **State file tampering**: write into the state file to inject a malicious provider → the next plan/apply triggers RCE
- **Atlantis Plan injection**: modify a `.tf` file in a PR to trigger `atlantis plan` → RCE on the Atlantis server
- **Atlantis Custom Workflow**: when `allow_custom_workflows=true`, `atlantis.yaml` can define arbitrary execution steps
- **Terraform Cloud Speculative Plan**: steal the TFC Token → trigger a speculative plan → execute code on the Runner → obtain the injected cloud credentials

→ read [references/platform-specific.md](references/platform-specific.md)

### 4.4 Other Platforms Quick Reference

| Platform | Key attack path | Details |
|---|---|---|
| GitLab CI | Runner Token theft, shared Runner escape, CI variable injection | → platform-specific.md |
| CircleCI | Context Secrets theft, SSH rerun, project variable import | → platform-specific.md |
| Azure DevOps | Service Connection Secrets, variable/parameter injection, Runner hijack | → platform-specific.md |
| Drone CI | `.drone.yml` commands injection, self-hosted Runner cloud/K8s permissions | → platform-specific.md |
| Buildkite | `.buildkite/*.yml` command injection, Agent cloud/K8s permissions | → platform-specific.md |
| Serverless Framework | IAM Role privilege escalation (AdministratorAccess by default), Plugin poisoning | → platform-specific.md |
| CloudFlare | Workers abuse, Zero Trust bypass | → platform-specific.md |
| Concourse / Airflow | Refer to the platform-specific.md quick reference table | → platform-specific.md |

## Notes

**OpSec:**
- CI/CD systems usually have complete audit logs — PR creation, workflow execution, and Secrets access are all recorded
- PRs on GitHub may still be picked up by a SIEM even after the account is deleted
- Actions on self-hosted Runners may trigger EDR/HIDS alerts
- In authorized testing, confirm the CI/CD test scope and impact with the client beforehand

**Bypassing Secrets protection:**
- GitHub Actions log masking only protects rendered output; the plaintext still exists in process memory
- Using base64 encoding or encryption bypasses most automatic masking mechanisms
- Derived data such as JWT signature values is not masked

**Escalating supply chain attacks:**
- Once an npm/PyPI publish token is stolen, malicious package versions can be published
- npm's `preinstall`/`postinstall` hooks execute automatically at install time
- Python's `.pth` files execute automatically when the interpreter starts
- A single CI/CD compromise can cascade across the entire supply chain (see the tj-actions/Ultralytics incident)
