---
name: cloud-k8s
description: "Authorized cloud, container, and Kubernetes security assessment: metadata SSRF, IAM misconfiguration, container escape paths, and cluster RBAC review."
zh-signals: "授权范围内开展云、容器与 Kubernetes 安全评估，涵盖元数据 SSRF、IAM 配置错误、容器逃逸与集群 RBAC 审查。信号:云安全,Kubernetes,容器逃逸,IAM,RBAC"
when-to-use: >-
  Use when assessing cloud workloads, containers, or Kubernetes clusters within an approved
  scope, including metadata SSRF, IAM misconfiguration, and RBAC review.
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# Cloud / Container / Kubernetes Security
## When to Use

- Assessing cloud workload or Kubernetes cluster security within an approved scope.
- Reviewing IAM/RBAC configurations for privilege-escalation paths.


## Applicable Scenarios

- Cloud metadata SSRF (169.254.169.254 / IMDS)
- Over-permissive IAM, public storage buckets, misconfigured security groups
- Docker/containerd escape path assessment
- Kubernetes RBAC, Secrets, Admission, supply chain images
- Container image vulnerabilities (can be linked with `supply-chain-security/`)

## Workflow

### Phase 1 — Identity and Boundaries

```text
□ Current identity: cloud AK/SK, K8s SA, node SSH?
□ Scope: single account / single cluster / single namespace
□ Network tier: authorized_target_only
```

### Phase 2 — Cloud Control Plane

```bash
# Example (replace per vendor; MUST stay within the authorized account)
aws sts get-caller-identity
aws s3 ls
# Corresponding identity commands for Azure / GCP
```

```text
□ Public buckets / misconfigured ACLs
□ Metadata: IMDSv1 vs v2; SSRF chains
□ Role assumption (PassRole) and lateral movement
```

### Phase 3 — Containers

```text
□ privileged / hostPath / hostNetwork present?
□ capabilities (SYS_ADMIN and similar)
□ Writable host paths → escape candidates
□ Image history and known CVEs → Trivy
```

### Phase 4 — Kubernetes

```bash
kubectl auth can-i --list
kubectl get pods,secrets,svc -A
kubectl get clusterrolebindings
```

```text
□ SA token mounting and permissions
□ Missing dangerous admission webhooks
□ etcd / dashboard exposure
□ Whether network policies default to allow
```

## Toolchain

| Tool | Purpose | Bootstrap |
|------|------|------|
| kubectl | Cluster interaction | Manual |
| trivy | Image/IaC | bootstrap `trivy` if available |
| kube-bench / kubeaudit | CIS/configuration | Manual |
| pacu / scoutsuite | Cloud audit (authorized) | Manual |
| nuclei | Known cloud vulnerability templates | bootstrap the nmap/nuclei ecosystem |

## References

- `references/k8s-cloud-checklist.md`
- CTF cross-reference: `../../CTF-Sandbox-Orchestrator/competition-agent-cloud/`
- `../supply-chain-security/` `../pentest-tools/`

## Routing Context

**Upstream**: MASTER R23  
**Downstream**: obtain a node shell → `attack-chain` / `windows-ad`; image vulnerabilities → supply-chain  
**MUST NOT**: scan other tenants of a public cloud without authorization

## Task Completion Self-Check

- [ ] Did you stay within the authorized account/cluster?
- [ ] Do the findings include reproduction and impact?
- [ ] Did you avoid destructive operations?
- [ ] Report / journal?

## Limitations

- Cloud provider API calls may incur cost and trigger alerts; coordinate with the owner.
- Escape-path validation must stay inside disposable lab clusters.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
