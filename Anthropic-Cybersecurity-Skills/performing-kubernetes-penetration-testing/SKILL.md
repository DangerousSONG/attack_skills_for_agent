---
name: performing-kubernetes-penetration-testing
description: "Perform Kubernetes penetration testing. Signals: cloud privilege escalation, iam privilege escalation, container privilege escalation."
zh-signals: "Performing Kubernetes Penetration Testing 信号:云提权,iam提权,容器提权。"
when-to-use: >-
  Evaluates Kubernetes cluster security by actively simulating attacker techniques against the
  API server, kubelet, etcd, pods, RBAC, network policy, and secrets, using kube-hunter,
  Kubescape, peirates, and manual kubectl exploitation to find paths to cluster compromise.
  Use for an authorized penetration test or hands-on validation that controls actually stop an
  attacker. Keywords: kube-hunter, Kubescape, peirates, kubelet 10250, anonymous auth, token
  theft, lateral movement, cluster takeover. Do not use for a configuration-only compliance
  audit - use performing-kubernetes-cis-benchmark-with-kube-bench.
domain: cybersecurity
subdomain: container-security
tags:
- containers
- kubernetes
- security
- penetration-testing
- offensive-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.IR-01
- ID.AM-08
- DE.CM-01
mitre_attack:
- T1610
- T1611
- T1609
- T1525
---
# Performing Kubernetes Penetration Testing

## Overview

Kubernetes penetration testing systematically evaluates cluster security by simulating attacker techniques against the API server, kubelet, etcd, pods, RBAC, network policies, and secrets. Using tools like kube-hunter, Kubescape, peirates, and manual kubectl exploitation, testers identify misconfigurations that could lead to cluster compromise.


## When to Use

- When conducting security assessments that involve performing kubernetes penetration testing
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Authorized penetration testing engagement
- Kubernetes cluster access (various levels for different test scenarios)
- kube-hunter, kubescape, kube-bench installed
- kubectl configured
- Network access to cluster components

## Core Concepts

### Kubernetes Attack Surface

| Component | Port | Attack Vectors |
|-----------|------|---------------|
| API Server | 6443 | Auth bypass, RBAC abuse, anonymous access |
| Kubelet | 10250/10255 | Unauthenticated access, command execution |
| etcd | 2379/2380 | Unauthenticated read, secret extraction |
| Dashboard | 8443 | Default credentials, token theft |
| NodePort Services | 30000-32767 | Service exposure, application exploits |
| CoreDNS | 53 | DNS spoofing, zone transfer |

### MITRE ATT&CK for Kubernetes

| Phase | Techniques |
|-------|-----------|
| Initial Access | Exposed Dashboard, Kubeconfig theft, Application exploit |
| Execution | exec into container, CronJob, deploy privileged pod |
| Persistence | Backdoor container, mutating webhook, static pod |
| Privilege Escalation | Privileged container, node access, RBAC abuse |
| Defense Evasion | Pod name mimicry, namespace hiding, log deletion |
| Credential Access | Secret extraction, service account token theft |
| Lateral Movement | Container escape, cluster internal services |

## Workflow

### Step 1: External Reconnaissance

```bash
# Discover Kubernetes services
nmap -sV -p 443,6443,8443,2379,10250,10255,30000-32767 target-cluster.com

# Check for exposed API server
curl -k https://target-cluster.com:6443/api
curl -k https://target-cluster.com:6443/version

# Check anonymous authentication
curl -k https://target-cluster.com:6443/api/v1/namespaces

# Check for exposed kubelet
curl -k https://node-ip:10250/pods
curl http://node-ip:10255/pods  # Read-only kubelet
```

### Step 2: Automated Scanning with kube-hunter

```bash
# Install kube-hunter
pip install kube-hunter

# Remote scan
kube-hunter --remote target-cluster.com

# Internal network scan (from within cluster)
kube-hunter --internal

# Pod scan (from within a pod)
kube-hunter --pod

# Generate report
kube-hunter --remote target-cluster.com --report json --log output.json
```

### Step 3: CIS Benchmark Assessment with kube-bench

```bash
# Run kube-bench on master node
kube-bench run --targets master

# Run on worker node
kube-bench run --targets node

# Check specific sections
kube-bench run --targets master --check 1.2.1,1.2.2,1.2.3

# JSON output
kube-bench run --json > kube-bench-results.json

# Run as Kubernetes job
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l app=kube-bench
```

### Step 4: Framework Compliance with Kubescape

```bash
# Install kubescape
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# Scan against NSA/CISA hardening guide
kubescape scan framework nsa

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
