---
name: k8s-network-recon
description: "Network reconnaissance and service discovery inside a Kubernetes cluster. Use after obtaining a pod shell, when you need to discover other services in the cluster or run internal K8s scanning. Covers DNS PTR reverse lookups, SRV record enumeration, AXFR zone transfers, and K8Spider usage. Use this skill whenever lateral reconnaissance inside a pod, hunting for hidden services, or determining attack targets is needed, even if the user never mentions DNS"
zh-signals: "在已获得 Pod Shell 后进行 Kubernetes 集群内网络侦察与服务发现，覆盖 DNS PTR 反查、SRV 枚举、AXFR 与 K8Spider。信号:K8s内网侦察,DNS反查,服务发现,K8Spider,SRV记录"
when-to-use: >-
  Use after obtaining a pod shell in a Kubernetes cluster when you need to
  discover internal services, scan the cluster network, or identify
  lateral-movement targets.
metadata:
  tags: "k8s,kubernetes,dns,recon,service-discovery,k8spider,cluster,internal recon,service discovery"
  category: "cloud"
---

→ Read [references/network-attacks.md](references/network-attacks.md)

# Network Reconnaissance Inside a Kubernetes Cluster

The first step of lateral movement in a K8s cluster is figuring out what other services are running. Because K8s uses DNS for service discovery and every Service and Pod has a predictable DNS name, the whole cluster can be enumerated systematically through DNS reverse lookups.

## K8s DNS Naming Rules

| Resource Type | DNS Format | Example |
|---------|---------|------|
| Service | `<svc>.<ns>.svc.cluster.local` | `redis.default.svc.cluster.local` |
| Pod | `<pod-ip-dashed>.<ns>.pod.cluster.local` | `10-244-0-5.default.pod.cluster.local` |
| Headless Service | `<pod-name>.<svc>.<ns>.svc.cluster.local` | `web-0.nginx.default.svc.cluster.local` |

> **Note**: The DNS suffix is not necessarily `cluster.local`; it depends on the cluster configuration. Check the `search` line in `/etc/resolv.conf`.

### SRV Records

The SRV records of a Service expose port information:
```bash
nslookup -type=srv <service>.<namespace>.svc.cluster.local
# Example output: service = 0 50 80 svc.ns.svc.cluster.local
# Even without the _proto prefix, all valid ports can be found
```

---

## Phase 1: Determine the Scan Scope

DNS PTR reverse lookups are per-IP — a /16 range has 65535 IPs, so blind scanning can take tens of minutes. Spend 30 seconds determining the Service CIDR to bring scan time from minutes down to seconds.

**First obtain entry point information (ordered by reliability, highest first)**
```bash
# 1. Environment variables (fastest, almost always present)
echo $KUBERNETES_SERVICE_HOST
env | grep -i service_host

# 2. DNS configuration (the nameserver address is usually inside the Service CIDR)
cat /etc/resolv.conf

# 3. DNS query (the returned API Server IP exposes the CIDR segment)
nslookup kubernetes.default.svc.cluster.local

# 4. Routing table/ARP (auxiliary inference)
cat /etc/hosts && ip route && arp -a 2>/dev/null

# 5. Avoid `ip addr` — virtual NICs injected by sidecars distort the judgement
```

Infer the Service CIDR from the IP you obtained.

### Subnet Range Selection Strategy
⚠️ **Never use /8 or larger** — 16M+ IPs can never be scanned and would waste the whole round.

Recommended scan granularity:
1. Use the `KUBERNETES_SERVICE_HOST` obtained above to determine the Service CIDR
2. Start with `/24` (256 IPs, completes in seconds); if there are no results, expand to `/16` (65K IPs, minutes)
3. Common Service CIDRs: `10.96.0.0/16`, `10.100.0.0/16`, `10.43.0.0/16` (K3s)
4. If `KUBERNETES_SERVICE_HOST` is `10.96.0.1`, scan `10.96.0.0/16`

---

## Phase 2: Batch DNS Scanning

### Using K8Spider (recommended)

```bash
# PTR reverse lookups + SRV records + multithreading, all scanning in one command
k8spider scan -subnet 10.100.0.0/24

# Larger ranges
k8spider scan -subnet 10.96.0.0/12    # default Service CIDR
k8spider scan -subnet 10.244.0.0/16   # Pod CIDR (Flannel default)
k8spider scan -subnet 10.42.0.0/16    # Pod CIDR (K3s default)
```

> **Alternative**: Some CTF environments ship `dnscan` preinstalled (usage: `dnscan -subnet <cidr>`). It is functionally similar but does not support SRV record enumeration. Prefer K8Spider.

### Manual Method When No Tool Is Available

```bash
# PTR reverse lookups (one IP at a time)
for i in $(seq 1 254); do
  nslookup 10.100.0.$i 2>/dev/null | grep -v "NXDOMAIN" | grep "name =" &
done; wait

# AXFR zone transfer (if CoreDNS allows it)
dig axfr cluster.local @$(grep nameserver /etc/resolv.conf | awk '{print $2}')

# Wildcard DNS (deprecated in newer CoreDNS, but may still work on older versions)
nslookup any.any.svc.cluster.local
```

---

## Phase 3: Exploit the Discovered Services

After discovering services, rank them by attack value:

1. **Direct flag/data services** (names containing flag, secret, internal) → curl them immediately
2. **Cluster control plane** (API Server 6443, etcd 2379, kubelet 10250) → unauthenticated access = cluster takeover
3. **Policy/Webhook services** (kyverno-svc, gatekeeper) → can extract injectable Secrets
4. **Monitoring/operations** (prometheus 9090, grafana 3000, dashboard 8443) → information disclosure + credentials
5. **Business services** (other custom services) → judge by name and port

```bash
# Access the discovered services
curl <service>.<namespace>.svc.cluster.local
curl <service>.<namespace>.svc.cluster.local:<port>

# Try multiple paths against high-value targets
curl -s http://<svc>:<port>/
curl -s http://<svc>:<port>/flag
curl -s http://<svc>:<port>/api/v1
curl -sk https://<svc>:<port>/
```

---

## Related Skills

After discovering services, load the corresponding skill based on the target type:
- Istio/Envoy related services → `Skill(skill="k8s-istio-bypass")`
- Kyverno/OPA Webhook → `Skill(skill="k8s-webhook-abuse")`
- NFS/EFS storage → `Skill(skill="k8s-storage-exploit")`
- API Server/Kubelet → `Skill(skill="k8s-container-escape")`
- Detailed K8Spider usage → `Skill(skill="k8spider")`

## Tool Quick Reference

| Tool | Purpose | Installation |
|------|------|------|
| K8Spider | Batch K8s DNS scanning (PTR+SRV+AXFR+multithreading) | `go install github.com/Esonhugh/k8spider@latest` |
| nslookup/dig | Manual DNS queries | built into the system |
| CDK | Container penetration toolkit (includes service discovery) | installed via f8x |
