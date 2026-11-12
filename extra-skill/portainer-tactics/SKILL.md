---
name: portainer-tactics
description: |
  Portainer post-exploitation methodology: default credential authentication bypass, user enumeration timing attack, Docker API privileged container escape RCE, host filesystem mounting.
  This skill must be used whenever the user mentions a Portainer vulnerability, Portainer RCE, Portainer Docker escape, Portainer authentication bypass, Portainer exploitation, or Portainer detection.
  It also applies when the user mentions Docker management panel vulnerabilities, container management platform exploitation, or Portainer CE/BE penetration testing.
zh-signals: "针对 Portainer 容器管理平台的后渗透与漏洞利用方法。信号:Portainer,Docker逃逸,默认凭据,用户枚举,特权容器"
when-to-use: >-
  Use when targeting a confirmed Portainer instance and needing default-credential access, user enumeration, Docker API abuse, or container escape.
metadata:
  tags: "Portainer,Docker,container-management,default-credentials,user-enumeration,SSRF,privileged-container-escape,RCE,Kubernetes"
  category: "postexploit"
  mitre_attack: "T1190,T1059,T1078"
---

# Portainer Exploitation Skill

- **Product**: Portainer (Docker/Kubernetes container management platform)
- **Default ports**: 9000 (HTTP), 9443 (HTTPS) | **Identification**: `/api/status` returns JSON | **FOFA**: `app="Portainer"`

## Vulnerability Overview

| Vulnerability ID | Affected versions | Vulnerability type | Exploitation condition | Impact |
|---------|---------|---------|---------|------|
| Default/weak credentials | All versions | Authentication bypass | Weak credentials | Critical |
| CVE-2024-29296 | CE 2.19.4 | User enumeration (timing) | No authentication required | Medium |
| CVE-2018-12678 | <=1.17 | Request Splitting SSRF→RCE | No authentication required | Critical |
| Docker API abuse | All versions | Privileged container escape RCE | Authentication required | Critical |

## Exploitation Decision Tree

```
1. Identify: GET /api/status → confirm Portainer
2. Authentication bypass:
   ├── Try default credentials admin/known password
   ├── CVE-2024-29296: user enumeration to determine valid usernames
   └── Brute force the password
3. After authentication: JWT Token → enumerate endpoints → privileged container → mount host → RCE
4. Unauthenticated (old versions): CVE-2018-12678 → Request Splitting → Docker API → RCE
```

## Exploit Chain Priorities

```
1. Default/weak credentials → JWT Token → Docker API → privileged container → RCE
2. CVE-2024-29296 user enumeration → targeted brute force → same as above
3. CVE-2018-12678 (only <=1.17) → SSRF → Docker API → RCE
```

## Common API Endpoints

| Endpoint | Purpose |
|------|------|
| `GET /api/status` | System status/version |
| `POST /api/auth` | Login authentication |
| `GET /api/endpoints` | Docker endpoint list |
| `POST /api/endpoints/{id}/docker/containers/create` | Create a container |
| `POST /api/endpoints/{id}/docker/containers/{cid}/start` | Start a container |
| `POST /api/endpoints/{id}/docker/containers/{cid}/wait` | Wait for a container |

## Privileged Container Escape Methodology

**Technique**: create a privileged container through the Portainer Docker API and mount the host filesystem to achieve container escape RCE.

- Abuse the Docker API `/containers/create` endpoint to create a container in privileged mode
- Mount the host root directory `/` into the container with read-write access
- Use `chroot` to switch to the host filesystem, so commands act directly on the host
- Requires an authenticated JWT Token and a usable Docker endpoint

## Detailed Reference

- [Post-auth RCE API quick reference](references/post-auth-rce.md)
