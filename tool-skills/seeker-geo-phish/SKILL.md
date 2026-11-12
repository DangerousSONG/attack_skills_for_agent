---
name: seeker-geo-phish
description: "seeker: precise phishing targeting. Signals: phishing, social engineering, custom phishing page, nearby WiFi phishing template."
zh-signals: "seeker: 精准定位钓鱼。信号:钓鱼,社会工程,手动定制钓鱼页,邻近 WiFi 钓鱼模板。"
when-to-use: "Use when running a phishing or social engineering campaign that needs precise target geolocation via a custom phishing page or nearby WiFi template. Requires a publicly reachable host and a chosen phishing template."
---

# seeker

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/thewhiteh4t/seeker
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/thewhiteh4t/seeker && cd seeker && chmod +x install.sh && ./install.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./seeker.py -t manual` | Manually customize the phishing page |
| `-t nearphish` | Nearby WiFi phishing template |
| `-k <key>` | Google Maps API key configuration |

## Attack Scenario Playbook

### Precise targeting for phishing

```bash
./seeker.py -t manual
# Generate a link and send it to the target; once they open it the browser geolocation prompt is triggered and the coordinates are sent back
```

## Notes

Relies on the target granting browser geolocation access; always use it within an authorized testing framework.
