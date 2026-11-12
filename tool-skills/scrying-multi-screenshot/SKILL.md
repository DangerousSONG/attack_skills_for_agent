---
name: scrying-multi-screenshot
description: "Scrying: Periodically captures target screenshots. Signals: screen capture, screenshots, single-target screenshot, RDP only, output directory."
zh-signals: "Scrying: 目标屏幕定时截图采集。信号:屏幕捕获,截图,单目标截图,仅 RDP,输出目录。"
when-to-use: >-
  Use when you need to periodically capture screenshots of RDP, VNC, and web
  targets in bulk to quickly locate admin panels or default pages; accepts Nmap
  XML output and an output directory.
---

# Scrying

- Attack Category: C34 Screen Capture and Forensics
- Upstream Repository: https://github.com/nccgroup/scrying
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install scrying or download the release
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `scrying --target https://t.com` | Single-target screenshot |
| `scrying -f targets.txt` | Batch (RDP/VNC/Web) |
| `--rdp` | RDP only |
| `-o out/` | Output directory |
| `--nmap xml` | Parse Nmap results |

## Attack Scenario Playbook

### Periodic Target Screen Capture

```bash
nmap -p 3389,5900,80,443,8080 --open 10.0.0.0/24 -oX n.xml
scrying -f n.xml -o shots/
# Quickly locate admin panels / default pages
```

## Notes

By NCC, batch screenshotting of RDP/VNC/Web services, a great fit for illustrations in security assessment reports.
