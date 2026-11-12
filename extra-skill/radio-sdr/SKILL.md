---
name: radio-sdr
description: "Authorized RF/SDR security research: signal identification, replay-feasibility study in shielded labs, and wireless protocol analysis outside regulated bands."
zh-signals: "在授权实验室环境中开展 RF/SDR 信号识别、重放可行性与无线协议分析。信号:RF,SDR,无线协议,信号识别,重放"
when-to-use: "Use for authorized RF/SDR research such as signal identification or replay-feasibility studies in shielded, RF-isolated labs."
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

# RF / SDR Security Research
## When to Use

- Lab study of wireless protocols with your own devices.
- Feasibility checks for replay attacks in RF-isolated environments.


## Applicable Scenarios

- Non-Wi-Fi RF such as wireless remotes and sensors (authorized)
- Protocol research on ADS-B / RC remotes (legal reception only)
- Division of labor with wifi-wireless: this skill focuses on **general-purpose SDR RF**; Wi-Fi attack and defense goes to R29

## Workflow

```text
□ Confirm applicable regulations and permits
□ Receive only: identify center frequency and modulation
□ Analyze with GNU Radio / URH
□ Replay only in a shielded room and with written permission
□ Conclusions focus on: whether unauthorized control is possible / hardening recommendations
```

## Toolchain

| Tool | Purpose |
|------|------|
| RTL-SDR / HackRF (compliant) | transmit/receive hardware |
| URH / GNU Radio | analysis |
| Inspectrum | signals |

## References

- `references/sdr-lab-rules.md`
- `../wifi-wireless/` `../ot-ics/` `../hardware-security/`

## Routing Context

**Upstream**: MASTER R38  
**MUST NOT**: interfering with public communications, unauthorized transmission

## Task Completion Self-Check

- [ ] Did you default to receive-only and record the regulatory boundary?
- [ ] Checklist?

## Limitations

- Transmitting on licensed frequencies is illegal without permits; shield and stay low-power.
- Protocol analysis quality depends on SDR bandwidth and sampling.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
