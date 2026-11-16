---
name: local-resources
description: "Navigation of the local resource library — wordlists (Dic), payload library, and POC library, with their structure and usage. Must read when using ffuf/spray for directory brute-forcing, password brute-forcing, or building fuzz payloads. Covers wordlist selection strategy, payload template invocation, and POC library search methods. All wordlists are installed under the /pentest directory"
zh-signals: "本地字典、Payload 与 POC 资源库导航，指导目录爆破、密码爆破与 Fuzz 字典选择。信号:字典库,payload,ffuf,spray,目录爆破,资源导航"
when-to-use: >-
  Use when you need a local wordlist, payload template, or POC reference for
  ffuf/spray directory brute force, password brute force, or fuzzing.
metadata:
  category: "general"
  tags: "dictionary,wordlist,payload,poc,ffuf,spray,resource,wordlist,tool"
---

# Local Resource Library Navigation

⚠️ **Core rule: wordlists live under /pentest** — the aboutsecurity wordlist library and the nuclei template library are both installed under `/pentest/`.

## 📁 Wordlist Library (Dic/) — Directory Brute-Force / Password Brute-Force / Parameter Fuzzing

### Toolchain
```bash
# List the wordlist categories
ls /pentest/AboutSecurity/Dic/
# List the web wordlist subcategories
ls /pentest/AboutSecurity/Dic/Web/
# Use a wordlist (example)
spray -u http://target -d /pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt
ffuf -u http://target/FUZZ -w /pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt
```

### Common Wordlist Quick Reference

| Scenario | Path | Lines |
|------|-------------------|------|
| Generic directory brute-force | `Web/Directory/Fuzz_common.txt` | ~5k |
| PHP file discovery | `Web/Directory/php/Fuzz_php.txt` | ~48k |
| PHP Top100 | `Web/Directory/php/Top100_php.txt` | ~100 |
| CTF URI fuzzing | `Web/CTF/Fuzz_uri.txt` | ~220 |
| CTF parameter fuzzing | `Web/CTF/Fuzz_param.txt` | ~44 |
| CTF SQL fuzzing | `Web/CTF/Fuzz_sql.txt` | ~94 |
| Admin panel paths | `Web/Directory/Fuzz_admin_dir.txt` | — |
| API paths | `Web/Directory/Fuzz_api.txt` | — |
| Backup files | `Web/File_Backup/` | — |
| Password Top100 | `Auth/password/top100.txt` | — |
| DNS subdomains | `Web/dns/` | — |

### Decision Tree: Which Wordlist Should You Use?

```
Is the target a web application?
├── CTF/lab range → Web/CTF/Fuzz_uri.txt (small and precise)
├── PHP site → Web/Directory/php/Fuzz_php.txt (comprehensive)
├── Generic site → Web/Directory/Fuzz_common.txt
├── Looking for an admin panel → Web/Directory/Fuzz_admin_dir.txt
├── Looking for APIs → Web/Directory/Fuzz_api.txt
└── Looking for backups → Web/File_Backup/

Is the target an authentication service?
├── Password brute-force → Auth/password/top100.txt
├── Username enumeration → Auth/username/
└── Specific service → Port/{mysql,ssh,rdp,...}/
```

## 📁 Payload Library — Vulnerability Validation Payloads

### Toolchain
```bash
# List the aboutsecurity wordlist categories
ls /pentest/AboutSecurity/Dic/
# List the nuclei template library
ls ~/nuclei-templates/
# Read a specific payload file
cat /pentest/AboutSecurity/Dic/SQL-Inj/bypass-waf.txt
```

### Available Categories
SQL-Inj | XSS | LFI | SSRF | XXE | RCE | 403 bypass | upload | CORS | HPP | SSI

## ⚠️ The Correct Workflow When Using External Tools

```
❌ Wrong: ffuf -u http://target/FUZZ -w /usr/share/wordlists/common.txt
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        Guessing the path, it most likely does not exist

✅ Correct:
1. ls /pentest/AboutSecurity/Dic/Web/Directory/  → confirm the wordlist exists
2. ffuf -u http://target/FUZZ -w /pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt
```

## 💡 Efficient Usage Tips

1. **spray / ffuf already wrap the wordlists** — for simple directory brute-forcing, use `spray -u target -d wordlist.txt` or `ffuf -u target/FUZZ -w wordlist.txt` directly
2. **Use ffuf for custom parameters** — when you need custom parameters (e.g. -e .bak -mc 200), use `ffuf -u target/FUZZ -w /pentest/AboutSecurity/Dic/...`
3. **Prefer small wordlists in CTF scenarios** — the wordlists under Web/CTF/ are streamlined and highly targeted, avoiding wasted time with large wordlists
