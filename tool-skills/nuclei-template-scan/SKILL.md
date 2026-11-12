---
name: nuclei-template-scan
description: "Scan CVEs and exposure surface, verify component vulnerabilities. Signals: web scanning, vulnerability scanning, single target, batch targets."
zh-signals: "nuclei: 全量 CVE 与暴露面扫描、定向验证某组件漏洞。信号:web扫描,漏洞扫描,单目标,批量目标。"
when-to-use: >-
  Use when you need template-based CVE and exposure scanning across single or
  many targets, or want to verify a specific component vulnerability. Requires
  updated community templates and optionally custom templates.
---

# nuclei

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/projectdiscovery/nuclei
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates   # sync the community template library
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-u URL` | Single target |
| `-l urls.txt` | Batch targets |
| `-t path/to/template.yaml` | Specify a custom template |
| `-tags cve,exposure` | Filter templates by tag |
| `-severity critical,high` | Filter by severity |
| `-rl 150` | Rate limit in requests per second, prevents bans |
| `-o result.txt` | Write output to a file |
| `-nc` | Disable colored output, easier for logs |

## Attack Scenario Playbook

### Full CVE and exposure surface scanning

```bash
nuclei -l targets.txt -severity critical,high,medium -rl 100 -o nuclei_result.txt
```

### Targeted verification of a component vulnerability

```bash
nuclei -u https://target.com -tags "apache,spring" -severity critical,high
nuclei -u https://target.com -t ~/nuclei-templates/cves/2024/CVE-2024-xxxx.yaml
```

### Chaining scan results into exploitation

```bash
cat nuclei_result.txt | grep -oE 'https?://[^ ]+' | sort -u > exposed.txt
```

## Notes

Lower false positive rate than comparable tools, and the output can be fed directly to exploitation tools; always rate limit with `-rl` in production environments; put custom templates in `~/nuclei-templates/`.
