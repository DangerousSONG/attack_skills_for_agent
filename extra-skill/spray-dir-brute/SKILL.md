---
name: spray-dir-brute
description: "High-performance directory brute forcing and fingerprinting with spray. Use when you need directory/file enumeration, backup file discovery, or fingerprinting against a web target. spray is the next-generation directory brute forcing tool by chainreactors, with 50%+ better performance than ffuf, supporting smart filtering, mask wordlists, resumable scans, and batch targets. Consider this skill for any scenario involving directory brute forcing, path enumeration, backup file scanning, or web fingerprinting"
zh-signals: "使用 spray 进行高性能目录爆破、路径枚举与 Web 指纹识别，支持智能过滤和批量目标。信号:目录爆破,路径枚举,备份文件扫描,指纹识别,spray工具"
when-to-use: "Use when you need fast directory or file brute forcing, backup file discovery, or web fingerprinting against one or many targets with spray."
metadata:
  tags: "spray,directory,brute,fuzz,directory brute forcing,path enumeration,backup file,fingerprinting,chainreactors,web scan"
  category: "tool"
---

# spray Directory Brute Forcing Methodology

spray is a high-performance directory brute forcing tool by chainreactors, whose core advantages are: **smart filtering** (automatically identifies invalid responses) + **extreme performance** (far beyond ffuf in multi-target scenarios) + **fingerprinting** (integrated gogo/fingerprinthub/wappalyzer fingerprint databases).

Project address: https://github.com/chainreactors/spray

## Phase 1: Basic Directory Brute Forcing

```bash
# Brute force from a wordlist (most common)
spray -u http://target -d wordlist.txt

# Multiple wordlists combined
spray -u http://target -d wordlist1.txt -d wordlist2.txt

# Specify suffixes
spray -u http://target -d wordlist.txt --suffix .php,.jsp,.asp

# Batch targets
spray -l urls.txt -d wordlist.txt
```

### Common wordlist paths (/pentest directory)

```bash
# aboutsecurity wordlist collection
/pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt
/pentest/AboutSecurity/Dic/Web/Directory/Fuzz_php.txt
/pentest/AboutSecurity/Dic/Web/CTF/Fuzz_param.txt

# spray's built-in wordlists are loaded automatically
```

## Phase 2: Mask Wordlist Generation

spray supports hashcat-like mask syntax, so there is no need to pre-generate wordlists:

```bash
# Masks: ?l=lowercase ?u=uppercase ?d=digits ?s=special characters
# Brute force /backup_XXXX.zip (4 digits)
spray -u http://target -w "/backup_{?d#4}.zip"

# Brute force /api/v1 through /api/v9
spray -u http://target -w "/api/v{?d#1}"

# Combined paths
spray -u http://target -w "/{?l#3}/{?l#4}.php"
```

## Phase 3: Smart Filtering

spray's core advantage — automatically filtering out invalid responses to reduce manual triage:

```bash
# Smart filtering (auto-detects 404 page signatures and filters them)
spray -u http://target -d wordlist.txt --smart

# Filter by status code
spray -u http://target -d wordlist.txt --match-status 200,301,302,403

# Filter by response length (exclude uniform error pages)
spray -u http://target -d wordlist.txt --filter-length 1234

# Filter by keyword
spray -u http://target -d wordlist.txt --match-string "admin"
```

## Phase 4: Fingerprinting Mode

spray integrates three fingerprint databases: gogo, fingerprinthub, and wappalyzer:

```bash
# check-only mode: fingerprinting only (similar to httpx)
spray -l urls.txt --check-only

# Enable extended fingerprinting (active probing + third-party fingerprint databases)
spray -u http://target --finger

# Brute forcing + fingerprinting
spray -u http://target -d wordlist.txt --finger
```

## Phase 5: Backup Files and Common Files

```bash
# Scan for backup files (.bak, .zip, .tar.gz, .sql, etc.)
spray -u http://target --bak

# Scan for common generic files (robots.txt, .git, .env, etc.)
spray -u http://target --common

# Full-feature scan (brute forcing + backups + common files + crawler + fingerprinting)
spray -u http://target -a
```

## Phase 6: Advanced Usage

```bash
# Enable the crawler (extracts more paths from pages)
spray -u http://target --crawl

# Resume an interrupted scan
spray --resume stat.json

# Custom header
spray -u http://target -d wordlist.txt -H "Cookie: session=xxx"

# Use a proxy
spray -u http://target -d wordlist.txt --proxy http://127.0.0.1:8080

# Control concurrency
spray -u http://target -d wordlist.txt -t 50
```

## Decision Table: spray vs ffuf

| Scenario | Recommended Tool | Rationale |
|------|---------|------|
| Single target directory brute forcing | Either spray or ffuf | Performance difference is small |
| Batch multi-target | **spray** | Batch performance far exceeds ffuf |
| Parameter fuzzing | **ffuf** | The FUZZ placeholder is more flexible |
| Backup file scanning | **spray** | One-shot scan with `--bak` |
| Fingerprinting | **spray** | Three built-in fingerprint databases |
| Mask wordlists needed | **spray** | Built-in mask generation |
