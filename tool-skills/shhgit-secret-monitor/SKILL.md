---
name: shhgit-secret-monitor
description: "shhgit: real-time GitHub leak monitoring. Signals: attack surface, cloud assets, scan local repos, CSV output."
zh-signals: "shhgit: Github 实时监控泄密。信号:攻击面,云资产,扫本地仓库,CSV 输出。"
when-to-use: >-
  Use when monitoring GitHub for secret leaks in real time or scanning a local
  repository and history for exposed credentials, with CSV output for triage.
---

# shhgit

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/eth0izzle/shhgit
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/eth0izzle/shhgit@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `shhgit --local path/to/repo` | Scan a local repository |
| `--live` | Monitor the GitHub event stream in real time |
| `-config config.yaml` | Configuration |
| `--csv-path out.csv` | CSV output |
| `--entropy-threshold 5.0` | Entropy threshold |

## Attack Scenario Playbook

### Real-Time GitHub Secret Monitoring

```bash
shhgit --live --csv-path leaks.csv  # Watch the full GitHub event stream for org keywords and key patterns
```

## Notes

Real-time mode requires a GitHub token; complements trufflehog (deep scanning) by providing broad monitoring.
