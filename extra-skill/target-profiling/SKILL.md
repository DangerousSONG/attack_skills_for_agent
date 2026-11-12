---
name: target-profiling
description: "Target panorama profiling and attack surface analysis. Use when you need to systematically organize target assets, generate a structured target profile, or share target information during multi-person penetration testing. Focuses on analysis and reporting rather than scanning itself. Suitable for deep analysis of data after recon-full"
zh-signals: "目标全景画像与攻击面分析，整理资产档案并支持多人协作共享。信号:目标画像,攻击面分析,资产整理,侦察报告"
when-to-use: >-
  Use when systematically organizing target assets, generating a structured target
  profile, or sharing target information in multi-person engagements, typically after
  recon is done.
metadata:
  tags: "recon,profiling,fingerprint,port,profiling,profile,asset analysis,attack surface assessment"
  category: "recon"
---

# Target Panorama Profiling Methodology

This skill complements `recon-full` (active scanning): recon-full handles "discovery", target-profiling handles "analysis and organization". If reconnaissance has not been done yet, run recon-full first.

## Phase 1: Data Aggregation
Use `evidence_list` (filter asset records by type) and `list_vulns` to obtain the existing reconnaissance data. If the data is insufficient, additionally run:
- `subfinder -d domain` / `ksubdomain -d domain` — subdomains
- `naabu -host target` — ports (nmap as an alternative)
- `httpx -u target -tech-detect` / `curl -sI target` — fingerprints

## Phase 2: Attack Surface Analysis

### 2.1 Technology Stack Distribution
Count the technology stacks used by the target and identify centrally managed versus independently deployed systems:
- Unified framework (e.g. the whole site runs Spring Boot) → one vulnerability may affect all systems
- Mixed technology stacks → evaluate each system independently

### 2.2 Exposure Assessment
Classify discovered services by risk level:

**Critical risk** (should be attacked first):
- Admin panels (admin/manager/console)
- Development/test environments (dev/staging/test)
- Exposed database ports (3306/5432/6379/27017)
- CI/CD systems (Jenkins/GitLab/Harbor)

**High risk**:
- Components with known vulnerabilities (old Spring/Struts/Log4j)
- Authentication pages (weak passwords/default credentials may exist)
- API endpoints (may lack authentication)

**Medium risk**:
- Standard web applications (need further manual testing)
- Mail/VPN entry points (social engineering entry points)

**Low risk**:
- CDN/static assets
- Purely informational websites

### 2.3 Network Topology Inference
Infer the network structure from the subdomain and IP distribution:
- Same IP range → possibly the same data center/VPC
- Real IPs behind a CDN → possibly able to bypass the WAF
- Mixed internal/external deployment → potential lateral movement paths

## Phase 3: Produce the Target Profile

Generate a structured report containing:
1. **Asset inventory**: domain/IP/port/service/version
2. **Technology stack overview**: framework/middleware/CMS distribution
3. **Attack priority**: a list of attack targets sorted by risk level
4. **Recommended attack paths**: based on the information found, suggest the 2-3 attack paths most likely to succeed
5. **Information gaps**: the aspects that still require further reconnaissance

## Network Topology Inference
- Subnet analysis: 10.0.1.x is likely the web segment (web servers in the same subnet), 10.0.2.x is likely the database segment (a different subnet, with network segmentation)

## Information Gap Identification
- Single-source subdomains: missing OSINT, missing crawler, insufficient coverage
- Incomplete ports: the default Top 1000 ports are not enough, a full port (65535) scan is required
- Non-standard ports (30000+) — high ports may hide services
