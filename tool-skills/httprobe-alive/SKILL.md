---
name: httprobe-alive
description: "httprobe filters subdomains to live sites. Signals: port scan, nmap, httprobe, concurrency, timeout ms."
zh-signals: "httprobe: 子域→存活站点过滤。信号:端口扫描,nmap,httprobe`,并发,超时 ms。"
when-to-use: "Use httprobe when filtering a list of subdomains or hosts into live HTTP/HTTPS services, typically as a pipeline stage before screenshotting or fingerprinting."
---

# httprobe

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/tomnomnom/httprobe
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/tomnomnom/httprobe@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat hosts.txt | httprobe` | Probe HTTP/HTTPS liveness in bulk |
| `-c 50` | Concurrency |
| `-t 10000` | Timeout in ms |
| `-p xlarge` | Large port set |
| `-s` | HTTPS only |

## Attack Scenario Playbook

### Subdomain to Live Site Filtering

```bash
subfinder -d corp.com -silent | httprobe -c 100 | tee alive.txt
cat alive.txt | aquatone  # downstream screenshotting/fingerprinting
```

## Notes

A standard component of the pd pipeline; stdin in, stdout out, integrates with other tools without friction.
