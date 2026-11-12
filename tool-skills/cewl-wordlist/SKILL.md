---
name: cewl-wordlist
description: "CeWL: Generates target-specific password dictionaries. Signals: password cracking, hash cracking, site-based dictionary generation, crawl depth, minimum length."
zh-signals: "CeWL: 目标定制口令字典。信号:密码破解,哈希破解,站点生成字典,爬深,最小长度。"
when-to-use: >-
  Use when you need a target-specific wordlist for password or hash cracking
  by crawling the target site. Supports crawl depth, word length bounds, email
  collection, and numeric variants.
---

# CeWL

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/digininja/CeWL
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install cewl
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cewl https://target.com -w custom.txt` | Site-based dictionary generation |
| `-d 3` | Crawl depth |
| `-m 8` | Minimum length |
| `-x 20` | Maximum length |
| `-e` | Collect emails |
| `-c` | Count word frequency |
| `--with-numbers` | Append numeric variants |

## Attack Scenario Playbook

### Target-Specific Password Wordlist

```bash
cewl https://corp.com -d 2 -m 6 -w corp_words.txt
hashcat -m 5600 ntlm.txt corp_words.txt --rules-file dive.rule
```

## Notes

Generates high-hit-rate wordlists from target site text; personal names, project code names, and slogans are all included.
