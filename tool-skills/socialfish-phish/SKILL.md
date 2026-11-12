---
name: socialfish-phish
description: "SocialFish: multi-platform phishing sites. Signals: phishing, social engineering, phishing platform, template."
zh-signals: "SocialFish: 多平台钓鱼站点。信号:钓鱼,社会工程,钓鱼平台,模板。"
when-to-use: "Use when building a phishing site for social engineering engagements and you need ready-made templates for multiple platforms managed from the SocialFish web panel."
---

# SocialFish

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/UndeadSec/SocialFish
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/UndeadSec/SocialFish && cd SocialFish && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 SocialFish.py -u admin -p pass` | Phishing platform |
| `-u u -p p -t` | Templates |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Multi-Platform Phishing Sites

```bash
python3 SocialFish.py
# 60+ site templates
```

## Notes

By UndeadSec, a multi-platform phishing framework.
