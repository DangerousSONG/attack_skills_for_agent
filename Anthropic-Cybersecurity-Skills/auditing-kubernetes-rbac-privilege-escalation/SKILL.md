---
name: auditing-kubernetes-rbac-privilege-escalation
description: "Audit Kubernetes RBAC privilege escalation. Signals: cloud privilege escalation, IAM privilege escalation, container privilege escalation."
zh-signals: "Auditing Kubernetes RBAC Privilege Escalation 信号:云提权,iam提权,容器提权。"
when-to-use: >-
  Finds over-permissive RBAC roles and service-account token abuse paths in a Kubernetes
  cluster using kubectl auth can-i, rbac-police, kubectl-who-can, and rakkess, tracing which
  subjects can escalate toward cluster-admin. Use when reviewing who can escalate privileges
  in a cluster, hunting exploitable RoleBindings during an authorized review, or validating
  least privilege after an RBAC change. Keywords: RBAC, ClusterRoleBinding, service account
  token, auth can-i, rbac-police, escalate, bind, impersonate. Do not use for designing and
  applying hardened RBAC - use implementing-rbac-hardening-for-kubernetes.
domain: cybersecurity
subdomain: container-security
tags:
- kubernetes
- rbac
- privilege-escalation
- service-account
- least-privilege
- kubectl
- access-control
- attack-paths
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AA-05
mitre_attack:
- T1078
---
# Auditing Kubernetes RBAC Privilege Escalation

> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Enumerating and exercising RBAC permissions affects a live cluster's access posture. Only test clusters you own or are explicitly authorized in writing to assess.

## Overview

Kubernetes Role-Based Access Control (RBAC, MITRE ATT&CK T1078 Valid Accounts) governs what every user and service account may do via `Role`/`ClusterRole` rules bound by `RoleBinding`/`ClusterRoleBinding`. Because workloads run with a mounted service-account token by default, an attacker who compromises one pod inherits that account's RBAC rights. Over-permissive bindings turn a single compromised pod into a cluster takeover: certain verbs and resources are "RBAC-equivalent to cluster-admin."

Per the Kubernetes "RBAC Good Practices" guidance and Unit 42 research, the dangerous primitives are:

- **`escalate` on roles** — grant yourself any permission, even ones you do not hold.
- **`bind` on clusterroles** — create a binding to `cluster-admin`.
- **`impersonate`** on users/groups/serviceaccounts — act as any subject including `system:masters`.
- **`create`/`update`/`patch` on `pods`** — schedule a privileged pod or mount the node, escaping to the host (T1611).
- **`create` on `pods/exec`, `pods/attach`, `pods/ephemeralcontainers`** — run code in any existing pod.
- **`get`/`list`/`watch` on `secrets`** — list returns full secret contents, including other service-account tokens.
- **`create` on `serviceaccounts/token`** — mint tokens for more privileged accounts.
- **`update`/`patch` on `validatingwebhookconfigurations`/`mutatingwebhookconfigurations`, `nodes/proxy`, `certificatesigningrequests/approval`** — admission/CSR abuse to cluster-admin.
- **Wildcards** (`verbs: ["*"]`, `resources: ["*"]`) — implicit super-privilege.

This skill systematically enumerates effective permissions for every subject, maps which subjects hold these escalation primitives, and produces remediation evidence. Source: Kubernetes RBAC Good Practices; Unit 42 Kubernetes RBAC research.

## When to Use

- During an authorized Kubernetes security assessment or cluster penetration test
- After compromising a pod, to determine what its service-account token can reach
- When reviewing RBAC drift before a production go-live
- When validating least-privilege after a platform migration or Helm rollout

## Prerequisites

- `kubectl` configured against the target cluster (your own credentials, or a captured service-account token)
- Read access to RBAC objects (most audits run with a cluster-reader or admin context)
- Audit tooling:
  ```bash
  # rbac-police - find escalation paths (Cymulate)
  curl -L https://github.com/PaloAltoNetworks/rbac-police/releases/latest/download/rbac-police-linux-amd64 -o rbac-police
  chmod +x rbac-police

  # kubectl-who-can - which subjects can perform an action (Aqua)
  kubectl krew install who-can

  # rakkess - access matrix of resources x verbs for the current/another subject
  kubectl krew install access-matrix

  # rbac-lookup - which roles a subject has (FairwindsOps)
  kubectl krew install rbac-lookup
  ```

## Objectives

- Inventory all `Role`, `ClusterRole`, `RoleBinding`, and `ClusterRoleBinding` objects
- Enumerate effective permissions per subject using `kubectl auth can-i --as`
- Identify subjects holding RBAC-equivalent-to-admin primitives
- Trace token-mounting pods to over-privileged service accounts
- Demonstrate (in a lab) one escalation path end-to-end
- Output a prioritized findings report with least-privilege remediation

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic |
|--------------|------|--------|
| T1078 | Valid Accounts | Defense Evasion / Persistence / Privilege Escalation |
| T1098 | Account Manipulation | Persistence |
| T1528 | Steal Application Access Token | Credential Access |
| T1613 | Container and Resource Discovery | Discovery |
| T1611 | Escape to Host | Privilege Escalation |

## Workflow

### Step 1: Inventory RBAC Objects

```bash
# All roles and bindings, cluster-wide
kubectl get clusterroles,clusterrolebindings -o wide
kubectl get roles,rolebindings --all-namespaces -o wide

# Dump full RBAC for offline analysis
kubectl get clusterroles,clusterrolebindings,roles,rolebindings \
  --all-namespaces -o yaml > rbac-dump.yaml

# Who is bound to cluster-admin?
kubectl get clusterrolebindings -o json | \
  jq -r '.items[] | select(.roleRef.name=="cluster-admin") |
         .metadata.name + " -> " + (.subjects // [] | map(.kind+"/"+.name) | join(","))'
```

### Step 2: Enumerate Effective Permissions per Subject

`kubectl auth can-i` is the authoritative check because it evaluates the live authorizer (RBAC + webhooks). Use `--as` to impersonate a subject (requires impersonate rights for the audit identity).

```bash
# Full access matrix for a service account
kubectl auth can-i --list \
  --as=system:serviceaccount:default:default

# Targeted dangerous-permission probes
kubectl auth can-i create pods --all-namespaces \
  --as=system:serviceaccount:dev:builder
kubectl auth can-i get secrets --all-namespaces \
  --as=system:serviceaccount:dev:builder
kubectl auth can-i create serviceaccounts/token -n kube-system \
  --as=system:serviceaccount:dev:builder
kubectl auth can-i '*' '*' --all-namespaces \
  --as=system:serviceaccount:dev:builder

# rakkess full verb x resource matrix for a subject
kubectl access-matrix --as system:serviceaccount:dev:builder
```

### Step 3: Hunt the Escalation Primitives

```bash

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
