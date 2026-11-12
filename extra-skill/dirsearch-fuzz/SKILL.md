---
name: dirsearch-fuzz
description: "Web directory and file brute-force enumeration with dirsearch. Use when you need to discover hidden directories, files, admin panels, or backup files. dirsearch ships high-quality wordlists and supports multiple extensions, recursive scanning, and status code filtering. Use this skill for any scenario involving directory enumeration, path discovery, admin panel hunting, or sensitive file discovery"
zh-signals: "使用 dirsearch 对 Web 目录与文件进行暴力枚举，发现隐藏路径、后台、备份文件与敏感资源。信号:目录扫描,路径枚举,后台发现,备份文件,dirsearch"
when-to-use: "Use when you need to discover hidden directories, files, admin panels, or backup files on a web target through directory brute-force enumeration with dirsearch."
metadata:
  tags: "dirsearch,directory,fuzz,directory scanning,path enumeration,admin panel discovery,file discovery,backup file,web"
  category: "tool"
---

# dirsearch Web Directory Enumeration Methodology

dirsearch is a feature-rich web directory brute-force enumeration tool. Core advantages: **built-in high-quality wordlists** + **multi-extension support** + **recursive scanning** + **smart filtering**.

Project URL: https://github.com/maurosoria/dirsearch

## Phase 1: Basic Scanning

```bash
# Scan with the built-in wordlist
dirsearch -u http://target.com

# Specify extensions
dirsearch -u http://target.com -e php,asp,aspx,jsp

# Specify a wordlist
dirsearch -u http://target.com -w /path/to/wordlist.txt

# Quiet output
dirsearch -u http://target.com --quiet
```

## Phase 2: Filtering and Matching

```bash
# Exclude status codes
dirsearch -u http://target.com -x 404,403,500

# Show only specific status codes
dirsearch -u http://target.com -i 200,301,302

# Filter by response size
dirsearch -u http://target.com --exclude-sizes 0B,4KB

# Filter by response content
dirsearch -u http://target.com --exclude-texts "Not Found"

# Recursive scanning (keep scanning subdirectories after a directory is found)
dirsearch -u http://target.com -r --recursion-depth 3
```

## Phase 3: Advanced Options

```bash
# Custom request headers
dirsearch -u http://target.com -H "Cookie: session=abc"

# With authentication
dirsearch -u http://target.com --auth admin:password --auth-type basic

# Use a proxy
dirsearch -u http://target.com --proxy http://127.0.0.1:8080

# Control threads
dirsearch -u http://target.com -t 50

# Batch targets
dirsearch -l urls.txt -e php,asp

# Random User-Agent
dirsearch -u http://target.com --random-agent

# Force extensions (do not use the %EXT% placeholder)
dirsearch -u http://target.com -f -e php,asp
```

## Phase 4: Output

```bash
# Plain text
dirsearch -u http://target.com -o results.txt --format plain

# JSON output
dirsearch -u http://target.com -o results.json --format json

# CSV output
dirsearch -u http://target.com -o results.csv --format csv
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| PHP site | `dirsearch -u http://target -e php -x 404` |
| Java site | `dirsearch -u http://target -e jsp,do,action -x 404` |
| Admin panel hunting | `dirsearch -u http://target -w admin-wordlist.txt` |
| Backup files | `dirsearch -u http://target -e bak,old,zip,tar.gz,sql` |
| Deep recursive scan | `dirsearch -u http://target -r --recursion-depth 3 -e php` |
