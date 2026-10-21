---
name: performing-ai-driven-osint-correlation
description: Use AI/LLM-based reasoning with Sherlock, theHarvester, and SpiderFoot
when-to-use: Use AI/LLM-based reasoning with Sherlock, theHarvester, and SpiderFoot
  to correlate OSINT findings—usernames, emails, social profiles, domain records,
  breach databases, and dark-web mentions—into unified, confidence-scored intelligence
  profiles with link analysis. Use when raw OSINT data from multiple sources needs
  merging into one target profile or resolving identity linkage across platforms.
domain: cybersecurity
subdomain: threat-intelligence
tags:
- osint
- ai-correlation
- threat-intelligence
- reconnaissance
- link-analysis
- target-profiling
- sherlock
- theharvester
- spiderfoot
- maltego
version: '1.0'
author: juliosuas
license: Apache-2.0
atlas_techniques:
- AML.T0051
- AML.T0054
- AML.T0056
nist_ai_rmf:
- MEASURE-2.7
- MEASURE-2.5
- GOVERN-6.1
- MAP-5.1
d3fend_techniques:
- Identifier Analysis
- URL Analysis
- Identifier Reputation Analysis
- User Behavior Analysis
- Content Validation
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
mitre_attack:
- T1591
- T1592
- T1593
- T1589
- T1595
---

# Performing AI-Driven OSINT Correlation

## When to Use

- You have collected raw OSINT data from multiple tools and sources but need to identify connections, contradictions, and patterns across them.
- You need to build a unified intelligence profile for a target entity (person, organization, or infrastructure) from fragmented data.
- Traditional manual correlation is too slow or error-prone for the volume of data collected.
- You want confidence-scored assessments of identity linkage across platforms rather than simple keyword matching.

## Prerequisites

- Python 3.10+ with `requests`, `json`, and `csv` libraries
- [Sherlock](https://github.com/sherlock-project/sherlock) installed (`pip install sherlock-project`)
- [theHarvester](https://github.com/laramies/theHarvester) installed (`pip install theHarvester`)
- [SpiderFoot](https://github.com/smicallef/spiderfoot) 4.0+ running on localhost:5001
- Access to an LLM API (OpenAI, Anthropic, or local model via Ollama)
- Optional: Maltego CE for graph visualization of correlation results
- Optional: API keys for Shodan, VirusTotal, HaveIBeenPwned, Hunter.io

## Workflow

### Legal & Ethical Requirements

- Obtain documented written authorization before any investigation
- Establish lawful basis for data processing (law enforcement, corporate policy, etc.)
- Define PII retention limits and data handling procedures
- Comply with local privacy regulations (GDPR, CCPA, etc.)

### Phase 1 — Multi-Source OSINT Collection

0. **Create the working directory for all OSINT outputs:**

   ```bash
   mkdir -p /tmp/osint
   ```

1. **Enumerate usernames across platforms with Sherlock:**

   ```bash
   sherlock "targetusername" --output /tmp/osint/sherlock-results.txt --csv
   ```

2. **Harvest emails, subdomains, and hosts with theHarvester:**

   ```bash
   theHarvester -d targetdomain.com -b all -f /tmp/osint/harvester-results.json
   ```

3. **Run a SpiderFoot passive scan via REST API:**

   ```bash
   curl -s http://localhost:5001/api/scan/start \
     -d "scanname=target-recon&scantarget=targetdomain.com&usecase=passive" \
     | jq '.scanid'
   ```

4. **Export SpiderFoot results when scan completes:**

   ```bash
   SCAN_ID="<scanid_from_step_3>"
   curl -s "http://localhost:5001/api/scan/${SCAN_ID}/results?type=all" \
     -o /tmp/osint/spiderfoot-results.json
   ```

5. **Query breach databases for email exposure (example with HIBP API):**

   ```bash
   curl -s -H "hibp-api-key: ${HIBP_KEY}" \
     -H "User-Agent: OSINT-Correlation-Skill" \
     "https://haveibeenpwned.com/api/v3/breachedaccount/target@example.com" \
     -o /tmp/osint/breach-results.json
   ```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
