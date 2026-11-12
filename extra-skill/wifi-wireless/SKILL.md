---
name: wifi-wireless
description: "Authorized wireless security assessment: Wi-Fi capture, WPA handshake analysis, rogue AP detection research, and lab-only deauthentication testing."
zh-signals: "授权无线安全评估技能，涵盖 Wi-Fi 抓包、WPA 握手分析、仿冒 AP 检测研究与实验环境去认证测试。信号:无线安全,WiFi,WPA握手,仿冒AP,去认证"
when-to-use: "Use for authorized wireless security assessments on networks you own or are cleared to test, including Wi-Fi capture, WPA handshake analysis, rogue AP detection, and lab-only deauthentication testing."
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# Wi-Fi / Wireless Security
## When to Use

- Assessing wireless posture of networks you own or are cleared to test.
- Studying handshake material captured on your own lab network.


## Applicable Scenarios

- Authorized Wi-Fi security assessment
- WPA/WPA2 handshake collection and offline assessment
- Rogue AP / evil-twin hotspot detection research
- Enterprise wireless isolation and captive portal security

## Workflow

```text
□ iwconfig / airmon-ng switch to monitor mode (legitimate environment)
□ airodump-ng lock onto the target BSSID channel
□ Handshake or PMKID capture (target only)
□ hashcat/aircrack offline assessment of password policy
□ Report: encryption type, isolation, portal bypass, recommendations
```

## Toolchain

| Tool | Purpose |
|------|------|
| aircrack-ng suite | capture/assessment |
| hcxdumptool / hcxtools | PMKID |
| hashcat | password assessment |
| Wireshark | management frame analysis |

## References

- `references/wireless-lab-rules.md`
- `../pentest-tools/` `../attack-chain/` (closely related chapters)

## Routing Context

**Upstream**: MASTER R29  
**MUST NOT**: unauthorized deauth, operating on non-target customer networks

## Task Completion Self-Check

- [ ] Did you strictly lock onto the target BSSID?
- [ ] Did you provide hardening recommendations in the report?
- [ ] Checklist?

## Limitations

- Deauthentication attacks are disruptive and illegal off-lab; lab use only.
- WPA3 changes several attack surfaces documented here for WPA2.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
