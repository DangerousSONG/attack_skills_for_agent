---
name: cameradar-rtsp
description: "Cameradar: Takes over surveillance cameras via weak passwords. Signals: VPN vulnerability, firewall, RTSP port scanning, specified ports, default credential dictionary."
zh-signals: "Cameradar: 监控摄像头弱口令接管。信号:vpn漏洞,防火墙,扫描 RTSP 端口,指定端口,默认凭据字典。"
when-to-use: >-
  Use when scanning a network for RTSP surveillance cameras and attempting
  default or common credentials to take over the stream; supports CIDR targets,
  custom ports, and credential dictionaries.
---

# Cameradar

- Attack Category: C11 Perimeter Device and VPN Attacks
- Upstream Repository: https://github.com/Ullaakut/cameradar
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
docker run -t ullaakut/cameradar -t 192.168.0.0/24 or go install
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-t target / CIDR` | Scan RTSP ports |
| `-p 554,8554` | Specify ports |
| `-r /dictionaries/credentials.json` | Default credential dictionary |
| `-s` | Disable screenshots |
| `-o /tmp/out` | Output |

## Attack Scenario Playbook

### Taking Over Surveillance Cameras with Weak Credentials

```bash
cameradar -t 10.0.0.0/24
# Automatically tries common RTSP credentials such as admin/admin and verifies the stream URL rtsp://ip:554/stream
```

## Notes

133 common camera credentials are built in by default; once you have the RTSP stream you can pull it with ffmpeg for evidence collection.
