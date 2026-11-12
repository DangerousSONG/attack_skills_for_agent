---
name: ffuf-web-fuzz
description: "ffuf fuzzes directories and parameters, including simultaneous multi-location payloads. Signals: web scanning, vulnerability scanning, wordlists, multiple wordlists, placeholders."
zh-signals: "ffuf: 目录与参数点 fuzz、多位置同时 fuzz(用户+ID)。信号:web扫描,漏洞扫描,字典文件,多字典多占位符。"
when-to-use: >-
  Use when fuzzing web paths, parameters, or multiple payload positions inside
  authenticated or unauthenticated applications; supply URL placeholders such
  as FUZZ and a wordlist, and enable auto-calibration to filter soft 404s.
---

# ffuf

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/ffuf/ffuf
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/ffuf/ffuf/v2@latest
# or apt install ffuf (bundled with Kali)
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-u URL/FUZZ` | The FUZZ placeholder is replaced line by line from the wordlist |
| `-w /path/wordlist.txt` | Wordlist file |
| `-w wl.txt:FUZZ2` | Multiple wordlists and multiple placeholders |
| `-mc 200,301,302` | Keep only the specified status codes |
| `-fc 404` | Filter out status codes |
| `-ac` | Auto-calibration, filters out soft 404s and similar pages |
| `-rate 100` | Global request rate limit |
| `-t 80` | Number of threads |
| `-recursion -recursion-depth 2` | Recursively discover new directories |
| `-H "Cookie: session=xxx"` | Scan backend functionality with an auth header |
| `-o result.json -of json` | JSON output for consumption by scripts |

## Attack Scenario Playbook

### Fuzzing directories and parameter points

```bash
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -ac -t 80
ffuf -u "https://target.com/api/FUZZ=test" -w params.txt -mc 200 -ac
```

### Simultaneous fuzzing at multiple locations (user + ID)

```bash
ffuf -u https://target.com/users/FUZZ/orders/FUZZ2 -w users.txt:FUZZ -w ids.txt:FUZZ2 -ac
```

### Scanning backend features with an authenticated session

```bash
ffuf -u https://target.com/admin/FUZZ -w endpoints.txt -H "Cookie: session=admin_token" -mc 200,302 -o admin_fuzz.json -of json
```

## Notes

The FUZZ placeholder is case sensitive (all caps); always enable `-ac` in the field or soft 404s will drown out the results; export results with `-of json` for further processing.
