---
name: argocd-tactics
description: |
  ArgoCD post-exploitation methodology: Redis cache poisoning cluster takeover, SSO authentication bypass, unauthorized API enumeration, malicious Application deployment, Webhook SSRF, default credential abuse.
  Must use this skill when the user mentions ArgoCD vulnerabilities, ArgoCD exploitation, ArgoCD RCE, ArgoCD Redis, ArgoCD unauthorized access, ArgoCD detection, or GitOps security.
  Also applies when the user mentions K8s continuous delivery, Kubernetes GitOps, ArgoCD cluster takeover, ArgoCD cache poisoning.
zh-signals: "ArgoCD 后渗透方法论，覆盖 Redis 缓存投毒集群接管、SSO 认证绕过、未授权 API 枚举、恶意 Application 部署、Webhook SSRF 与默认凭据利用。信号:ArgoCD,Kubernetes,GitOps,缓存投毒,SSO绕过,SSRF"
when-to-use: >-
  Use when encountering ArgoCD-related vulnerabilities, exploitation, unauthorized API
  access, Redis cache poisoning, SSO bypass, or GitOps/Kubernetes delivery security issues.
metadata:
  tags: "ArgoCD,Kubernetes,GitOps,Redis,cache poisoning,SSO bypass,SSRF,K8s cluster takeover,continuous delivery,unauthorized API"
  category: "postexploit"
  mitre_attack: "T1190,T1078"
---

# ArgoCD Exploitation Skill

- **Product**: Argo CD (declarative GitOps continuous delivery tool for Kubernetes)
- **Default ports**: 80/443 (Web UI), 8080 (Server), 6379 (Redis)
- **Fingerprints**: page title "Argo CD", `/api/v1/version` returns version information
- **Default credentials**: admin / auto-generated initial password
- **FOFA**: `app="Argo-CD"` | **Shodan**: `http.title:"Argo CD"`

## Vulnerability Overview

| CVE | Affected versions | Type | Condition | Impact |
|-----|---------|------|------|------|
| CVE-2024-31989 | <2.11.5 | Redis cache poisoning → K8s takeover | Redis unauthenticated | Critical (9.1) |
| CVE-2022-29165 | <2.3.1 | SSO authentication bypass | OIDC SSO configured | High (8.8) |
| CVE-2023-22482 | multiple versions | Redis information disclosure | Redis unauthenticated | High (7.5) |
| CVE-2024-40638 | multiple versions | Webhook SSRF | authenticated user | High (7.2) |
| Default credentials | all versions | initial admin password | obtain the initial password | Critical |

## Exploitation Decision Tree

```
1. Identify ArgoCD → /api/v1/version
2. Unauthorized API → /api/v1/applications, /api/v1/clusters
3. CVE-2024-31989 (prefer) → Redis cache poisoning → cluster takeover
4. Default credentials → admin + initial password → full control
5. CVE-2022-29165 (SSO environment) → redirect_uri bypass
6. CVE-2024-40638 → Webhook SSRF
7. Post-authentication exploitation → malicious Application / manifest injection / privilege bypass
```

## Exploit Chain Priority

```
1. Redis unauthenticated → CVE-2024-31989 cache poisoning → K8s cluster takeover
2. Default credentials / weak credentials → full ArgoCD control
3. Unauthorized API → application/cluster/repository information disclosure
4. CVE-2022-29165 → SSO authentication bypass
5. CVE-2024-40638 → Webhook SSRF → internal service probing
6. Authenticated → create malicious Application → privileged Pod deployment
```

## Common Endpoint Quick Reference

| Endpoint | Method | Purpose | Auth |
|------|------|------|------|
| `/api/v1/version` | GET | version information | not required |
| `/api/v1/applications` | GET | application list | optional |
| `/api/v1/clusters` | GET | cluster list | optional |
| `/api/v1/repositories` | GET | repository list | optional |
| `/api/v1/account` | GET | account information | optional |
| `/auth/login` | GET | login page | not required |
| `Redis 6379` | - | cache service | no password by default |

## Detailed Reference

- [Detection scripts and post-exploitation techniques](references/detection-and-post-exploit.md) - unauthorized API detection, comprehensive scanning scripts, post-authentication exploitation techniques
