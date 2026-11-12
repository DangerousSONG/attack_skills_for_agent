---
name: recon-full
description: "Active end-to-end asset reconnaissance. Use when a complete zero-to-vulnerability-discovery reconnaissance is needed for a target, for the first phase of a penetration test, or when a full picture of the target attack surface is required. Covers the full chain of subdomain enumeration → port scanning → liveness detection → fingerprinting → POC scanning"
zh-signals: "面向目标执行从子域名枚举到端口扫描、存活探测、指纹识别与 POC 扫描的主动式全流程资产侦察。信号:资产侦察,子域名枚举,端口扫描,指纹识别,POC扫描"
when-to-use: >-
  Use when performing the first reconnaissance phase against a target, needing a
  full asset-discovery-to-vulnerability chain, or mapping the attack surface
  starting from a domain or IP.
metadata:
  tags: "recon,subdomain,port,fingerprint,poc,scanning,reconnaissance,asset-discovery,attack-surface,penetration-testing,nmap"
  category: "recon"
  mitre_attack: "T1595,T1592,T1590,T1589"
---

# Active End-to-End Reconnaissance Methodology

This skill is the standard first step of a penetration test. The goal is to start from a domain/IP and discover as many assets and vulnerabilities as possible.

## Further Reading

- Web directories, historical endpoints, hidden parameters, Next.js/SPA route discovery → [references/web-discovery-methods.md](references/web-discovery-methods.md)

## Phase 0: Scope Confirmation

Confirm the scope of the test target against the task description, and stay within that scope as much as possible
- If the task states that subdomains must not be tested, skip Phase 1: subdomain enumeration
- If the task states that other ports must not be tested, skip Phase 2: port scanning

## Phase 1: Subdomain Enumeration
Use DNS enumeration tools to obtain more subdomains. This step is critical — subdomains are often forgotten attack surface (test environments, legacy versions, internal systems).

Recommended tools
- ksubdomain

**Analysis points**:
- Subdomain naming patterns: `dev.`, `test.`, `staging.`, `api.`, `admin.` are usually high-value targets
- CDN footprint: domains behind a CDN may require finding the origin IP
- Wildcard records: when `*.example.com` exists, enumeration with a wordlist is required instead of pure DNS resolution

## Phase 2: Port Scanning
Use a port scanning tool to scan the ports of the discovered IPs/domains.

Recommended tools
- naabu

**High-value ports**:
- Web: 80, 443, 8080, 8443, 8888
- Databases: 3306(MySQL), 5432(PostgreSQL), 6379(Redis), 27017(MongoDB)
- Remote administration: 22(SSH), 3389(RDP), 5900(VNC)
- Middleware: 8009(AJP/Tomcat), 9200(Elasticsearch), 2375(Docker API)

**Recommendations**
- If the scan indicates that the target exposes no open ports at all, use a full port scan (1-65535)
- Unless no tool is available at all, nmap is not recommended — it is too slow and performs poorly

## Phase 3: Liveness Detection
Use the urlive liveness probe to check whether HTTP/HTTPS services are alive.

Recommended tools
- httpx

**Analysis points**:
- HTTP to HTTPS redirect chains
- Different ports serving different applications (multiple sites per IP)
- Endpoints returning 403/401 → possibly an authenticated admin console
- 302 redirects to a login page → indicates protected content

## Phase 4: Fingerprinting
Use a fingerprinting tool to identify the technology stack, which directly determines the exploitation direction.

Recommended tools
- nuclei

**Technology stack → attack strategy mapping**:
| Technology stack | Priority checks |
|--------|----------|
| PHP | LFI/file upload/deserialization |
| Java/Spring | Deserialization/JNDI/Actuator |
| Python/Django/Flask | SSTI/Pickle |
| Node.js/Express | Prototype pollution/SSRF |
| WordPress/Joomla | CMS-specific POCs |
| Nginx/Apache | Parsing vulnerabilities/misconfiguration |

## Phase 5: POC Scanning
Use a vulnerability scanner to scan for known vulnerabilities. Focus on specific vulnerability classes based on the fingerprinting results.

Recommended tools
- nuclei

Common vulnerability types
- Framework vulnerabilities (Spring4Shell, Struts2, Log4j)
- CMS vulnerabilities (WordPress plugin, Joomla, Drupal)
- Middleware vulnerabilities (Tomcat Manager, WebLogic, JBoss)

## Output Requirements
Summarize the findings briefly at the end of each phase, and finally sort them by attack priority:
1. Directly exploitable high-severity vulnerabilities
2. Exposed admin consoles and sensitive interfaces
3. Attack surface that can be probed further
