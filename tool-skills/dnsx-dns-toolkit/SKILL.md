---
name: dnsx-dns-toolkit
description: "dnsx: subdomain liveness, record enumeration, and SPF/DMARC email spoof surface assessment. Signals: subdomain, domain enumeration, bulk resolution, show responsive only, retry count."
zh-signals: "dnsx: 子域存活+记录枚举、SPF/DMARC 邮件 spoof 面评估。信号:子域名,域名枚举,批量解析,只显示有响应的,重试次数。"
when-to-use: "Use during DNS reconnaissance for bulk subdomain resolution, record enumeration, and SPF/DMARC email spoofing surface assessment. Requires a host list and works best piped from subfinder or naabu."
---

# dnsx

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/projectdiscovery/dnsx
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-l subdomains.txt` | Bulk resolution |
| `-resp` | Only show responsive hosts |
| `-a -aaaa -cname` | Pull A/AAAA/CNAME records |
| `-txt` | Pull TXT records (SPF/verification token leaks) |
| `-retry 3` | Number of retries |
| `-rcode noerror,servfail` | Filter by response code |
| `-mx -ns` | MX/NS records |

## Attack Scenario Playbook

### Subdomain liveness and record enumeration

```bash
subfinder -d target.com | dnsx -a -aaaa -cname -txt -resp -o resolved.txt
```

### SPF/DMARC email spoof surface assessment

```bash
dnsx -d target.com -txt -resp | grep -i spf
dig _dmarc.target.com txt +short
```

## Notes

Part of the projectdiscovery ecosystem and pipes most smoothly from subfinder/naabu; -resp filters out NXDOMAIN noise.
