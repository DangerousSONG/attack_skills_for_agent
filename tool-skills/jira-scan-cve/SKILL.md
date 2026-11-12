---
name: jira-scan-cve
description: "jira_scan batch-checks Jira vulnerabilities. Signals: web vulnerability, injection, detect anonymous access, silent mode."
zh-signals: "jira_scan: Jira 漏洞批量核查。信号:web漏洞,注入,检测匿名访问,静默。"
when-to-use: "Use when assessing a Jira or Atlassian instance for known CVEs, anonymous access, and exploitable endpoints. Requires a target URL and optionally silent mode."
---

# jira_scan

- Attack Category: C09 Web Exploitation (CVE Exploitation)
- Upstream Repository: https://github.com/bcoles/jira_scan
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/bcoles/jira_scan && gem install jira_scan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `jira-scan -u 'https://jira.t.com'` | Detect Jira unauthenticated access / vulnerabilities such as CVE-2019-11581 |
| `-u url -c` | Detect anonymous access |
| `-q` | Quiet |

## Attack Scenario Playbook

### Jira Vulnerability Batch Check

```bash
cat jira_hosts.txt | xargs -I{} jira-scan -u {}
# A hit on CVE-2019-11581 (SMTP injection RCE) can be weaponized further
```

## Notes

A Jira/Atlassian CVE scanner that outputs affected versions and exploitable endpoints.
