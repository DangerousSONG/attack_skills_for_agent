---
name: witnessme-web-shot
description: "WitnessMe: Web asset full-page screenshots. Signals: screen capture, screenshot, single URL screenshot, batch, start web service to view results."
zh-signals: "WitnessMe: Web 资产整段截图。信号:屏幕捕获,截图,单 URL 截图,批量,起 Web 服务看结果。"
when-to-use: >-
  Use when you need to capture full-page screenshots of many web assets for
  reporting or attack-surface visualization; accepts a URL list and serves
  results through a web panel.
---

# WitnessMe

- Attack Category: C34 Screen Capture and Forensics
- Upstream Repository: https://github.com/byt3bl33d3r/WitnessMe
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install witnessme
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `witnessme snapshot -t https://t.com` | Single URL screenshot |
| `witnessme snapshot -f urls.txt` | Batch |
| `witnessme server -p 8080` | Start a web service to view the results |
| `--no-http` | HTTP(S) only |

## Attack Scenario Playbook

### Full-page screenshots of web assets

```bash
cat subdomains.txt | witnessme snapshot -f -
# Produces a web panel with thumbnails, ready for reporting
```

## Notes

By byt3bl33d3r, headless Chrome batch webpage screenshots plus a server-side viewer for visualizing the web attack surface.
