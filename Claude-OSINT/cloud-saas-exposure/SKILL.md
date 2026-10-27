---
name: cloud-saas-exposure
description: "组织级云与供应链暴露面发现:S3/GCS/Azure Blob 桶发现与接管、AWS 账户ID离线恢复、npm/PyPI 依赖混淆确认、云原生/K8s/CI 控制面指纹,纯被动。信号:云资产,暴露面。"
when-to-use: "Organization-grade cloud and supply-chain attack-surface discovery: S3/GCS/Azure Blob bucket discovery via observed-name mining (CNAME/cert-SAN/Wayback) and bounded two-class permutation (6 prefixes 
version: 1.0
sources: asm_reference_impl, public_research
triggers:
  - cloud attack surface
  - cloud exposure
  - SaaS exposure
  - cloud bucket enumeration
  - S3 bucket enum
  - GCS bucket enum
  - Azure blob enum
  - bucket takeover
  - dangling CNAME bucket
  - public cloud bucket
  - listable bucket
  - bucket ownership
  - object storage exposure
  - bucket permutation
  - AWS account ID
  - AWS account ID from access key
  - AKIA decode
  - access key account ID
  - offline AWS decode
  - base32 AWS account
  - AWS account enumeration
  - cross-account trust
  - IAM role phishing
  - sts assume role
  - dependency confusion
  - npm dependency confusion
  - PyPI dependency confusion
  - supply chain attack surface
  - unclaimed package
  - internal package registry
  - private npm registry
  - scoped npm package
  - npm scope claimability
  - package registry leak
  - cloud native fingerprint
  - Lambda function URL
  - API Gateway exposure
  - Cloud Run exposure
  - App Service exposure
  - serverless exposure
  - Kubernetes exposure
  - K8s exposure
  - kubelet exposure
  - etcd exposure
  - Docker API exposure
  - CI CD exposure
  - Jenkins exposure
  - GitLab exposure
  - control plane exposure
  - cloud footprint
  - cloud account attribution
---

# Cloud & SaaS Exposure — Buckets, Offline AWS Account-ID Recovery, Dependency Confusion, and Cloud-Native/K8s Fingerprinting

> Companion skills: `osint-methodology` (the pipeline this plugs into — Stage 2 asset
> expansion, Stage 4 exposure analysis, Stage 5 supply-chain confirmation). `offensive-osint`
> §16.8 (bucket-permutation raw wordlist), §16.17 (cloud-native URL pattern table), §16.18–
> §16.19 (container/K8s/CI paths + active curl recipes), §44 (package-registry search). This
> skill does not repeat those lists — it builds the reasoning layer on top: the
> ownership-gated bucket severity model, the offline AKIA→account-ID decode, the
> dependency-confusion two-part confirmation contract, and cloud-native/K8s as an
> org-attribution surface, not just another probe list.

## 0. When to Use / When NOT

**Use this skill when:** you're mapping an authorized target's cloud and supply-chain
footprint — enumerating storage buckets and judging whether a hit is actually the target's
risk (not a stranger's public bucket that happens to match a permutation); recovering the
AWS account ID behind a leaked access key you already hold (dead or live); confirming
whether an internal-looking npm/PyPI dependency is a registerable supply-chain vector; or
fingerprinting cloud-native (Lambda/Cloud Run/App Service/…) and container/K8s/CI
control-plane surface for org attribution and exposure triage.

**Do NOT use this skill when:** you just need the raw bucket-permutation wordlist,
cloud-native URL pattern table, or container/K8s/CI path list with no reasoning layer — go
straight to `offensive-osint` §16.8/§16.17–16.19/§44. Do NOT use it for anything past
discovery/confirmation: registering an unclaimed package, submitting AWS credentials,
authenticating to a Kubernetes API, or confirming a fingerprinted control plane actually
answers unauthenticated (that's a stage-6 `--validate --validate-cloud` active tier —
described, never performed, §5/§9.4).

---

## 1. Authorization & Legal Posture

Reuses `osint-methodology` §1 — assets you own or have written authorization to assess.
Three of this skill's four subsystems carry a distinct authorization shape, worth being
explicit about before you run any of them:

- **Bucket probing (§6)** is a real HTTP GET against bucket infrastructure that may or may
  not be the target's — the same "active but low-intrusion" tier as any other GET against
  target-adjacent infra. Standard engagement authorization applies.
- **AWS account-ID decode (§7)** is fully offline. No authorization question beyond already
  lawfully holding the leaked key.
- **Dependency-confusion confirmation (§8)** issues live GETs, but only against the public
  npm/PyPI registries — **zero packets to the target**. This is why it's explicitly in scope
  even though it's "active."
- **Cloud-native/K8s/CI fingerprinting (§9)** is pattern-matching over hostnames and ports
  already resolved by earlier recon — no new network traffic of its own.

---

## 2. Confidence Levels

Reuses `osint-methodology` §2. Domain-specific anchors:

| Level | Cloud/SaaS example |
|---|---|
| **TENTATIVE** | Org-namespace-matched dependency name (medium strength) with no private-registry binding — namesake-prone. |
| **FIRM** | Bucket exists (403/private) and is name-tied or CNAME/SAN/Wayback-observed; AWS account ID offline-decoded from a leaked key with no live validation; cloud-native endpoint pattern-matched via an owned CNAME/cert-SAN/subdomain FQDN; a container/K8s orchestration port is open (directly observed — its auth posture is not). |
| **CONFIRMED** | Bucket is publicly listable/readable **and** ownership-verified; AWS account ID corroborated by a live STS-validated key; dependency-confusion "strong" signal (private-registry binding) confirmed unclaimed via the public-registry 404 + scope-claimability check. |

An **unattributable** public bucket hit does not get a confidence label at all — it never
reaches the finding stream (§6.3).

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
