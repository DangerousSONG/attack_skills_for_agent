---
name: red-team-assessment
description: "End-to-end red-team assessment methodology. Use when starting a complete penetration test project or red-team assessment and you need the full orchestration from reconnaissance to reporting. Suitable for external foothold acquisition, security assessment projects, and periodic penetration tests. This skill handles task scheduling — invoke specialized skills for specific exploitation, and do not perform deep vulnerability testing inside this skill"
zh-signals: "红队评估全流程编排，从侦察到报告，适用于外网打点与定期渗透测试。信号:红队评估,渗透测试流程,外网打点,任务编排,安全评估"
when-to-use: "Use when starting a full penetration test or red-team assessment and you need end-to-end orchestration from reconnaissance to reporting, delegating exploitation to specialized skills."
metadata:
  tags: "red-team,assessment,pentest,security-assessment,end-to-end,foothold,automation,pentest"
  category: "general"
---

# Red Team Assessment End-to-End Methodology

This skill is the **overall process orchestration** for a penetration test — it does not contain specific exploitation techniques (those live in the specialized skills under exploit/), but it guides you to advance the entire assessment in the right order and with the right strategy.

## Phase 1: Passive Reconnaissance (Zero Contact)

Gather intelligence without touching the target:

1. **OSINT search engines**
   - Query the FOFA / Quake / Hunter APIs through `http_request` or `curl` for cross-engine searching
   - Target: an inventory of IP/domain assets, exposed services, and the technology stack

2. **Public information gathering**
   - Search GitHub/GitLab for organization names and domains (may leak source code / credentials)
   - Job posting analysis (leaks the technology stack and internal systems)
   - SSL certificate transparency logs (find subdomains)

**Output**: initial asset inventory + technology stack overview

## Phase 2: Active Reconnaissance

Based on the passive reconnaissance results, actively probe in a targeted way:

1. **Subdomain enumeration** — `subfinder` / `ksubdomain`
2. **Port scanning** — `naabu` (focus on high-value ports, nmap as a fallback)
3. **Live host detection** — `httpx` (confirm HTTP services)
4. **Fingerprinting** — `httpx -tech-detect` / `nuclei -t technologies/` (technology stack → determines the attack direction)
5. **Directory brute-forcing** — `spray` / `ffuf` (discover hidden entry points)

**Output**: a complete asset map (domain + IP + port + technology stack + hidden paths)

## Phase 3: Vulnerability Discovery

### 3.1 Automated Scanning
- `nuclei -u TARGET -severity critical,high` — Nuclei POC scanning
- `nuclei -u TARGET -t default-logins/` — default credential detection

### 3.2 Manual Testing (By Asset Type)
For each web application, select specialized tests based on the technology stack:

| Finding | Test Direction |
|------|----------|
| Login page | SQL injection, weak passwords |
| Search / query function | SQL injection, XSS |
| File upload | File upload bypass |
| API endpoint | IDOR, authentication bypass |
| Template rendering | SSTI |
| JWT token | JWT attacks |
| Java application | Deserialization |

### 3.3 Key Decisions
- **Breadth first**: run a quick scan across all assets first and mark every possible entry point
- **Deep attacks**: pick the 2-3 entry points most likely to yield a foothold and test them deeply
- Do not get stuck on a single point — after 3-5 rounds without progress, change direction

## Phase 4: Exploitation and Validation

After discovering a vulnerability, validate the exploitation:
1. Confirm the vulnerability is exploitable (PoC validation)
2. Assess the impact scope (data leak / RCE / privilege escalation)
3. If you obtain a shell → proceed with post-exploitation
4. Record the complete exploitation steps (for reproduction)

## Phase 5: Report Output

Produce the formal report.

**Key principles**:
- Order the findings by risk level (critical > high > medium > low > informational)
- Every finding must have: description, impact, reproduction steps, remediation recommendation
- The executive summary uses non-technical language
- The appendix contains the tool list and detailed technical data

## Recommended Time Allocation
| Phase | Time Share |
|------|----------|
| Passive + active reconnaissance | 20% |
| Vulnerability discovery | 30% |
| Exploitation validation | 35% |
| Reporting | 15% |

## Time Management Strategy
- Fast testing mode: complete within a 30-minute or 60-minute time limit
- Prioritize the easiest and most effective attack path, then move on to complex vulnerabilities
- When time is limited, focus on efficiency and ROI and allocate resources sensibly
- When you hit a bottleneck, change path (pivot): switch the attack surface, abandon the current path, and turn to another attack surface
- Look for alternative approaches and new entry points
