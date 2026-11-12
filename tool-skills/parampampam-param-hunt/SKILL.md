---
name: parampampam-param-hunt
description: "Find hidden debug parameters. Signals: web vulnerability, injection, hidden GET parameters, POST parameters, custom wordlist."
zh-signals: "ParamPamPam: 挖隐藏调试参数。信号:web漏洞,注入,发现隐藏 GET 参数,POST 参数,自定义字典。"
when-to-use: >-
  Use when hunting for hidden GET or POST parameters on a web endpoint using a
  wordlist, often to find debug or admin switches. Supports concurrency and
  custom wordlists.
---

# ParamPamPam

- Attack Category: C09 Web Exploitation (Parameter Discovery)
- Upstream Repository: https://github.com/Bo0oM/ParamPamPam
- Upstream License: WTFPL (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Bo0oM/ParamPamPam && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 parampampam.py -u 'https://t.com/page.php'` | Discover hidden GET parameters |
| `-m POST` | POST parameters |
| `-w params.txt` | Custom wordlist |
| `-c 20` | Concurrency |

## Attack Scenario Playbook

### Hunting for hidden debug parameters

```bash
python3 parampampam.py -u 'https://t.com/search.php' -c 50
# Manually test the admin/debug/export style parameters that hit
```

## Notes

Brute-forces undisclosed GET/POST parameters, often used to find backdoor switches such as debug=1.
