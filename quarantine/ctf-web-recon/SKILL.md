---
name: ctf-web-recon
description: "Recon methodology dedicated to CTF web challenges. Use when facing a CTF lab target and needing to quickly discover attack entry points. Unlike real-world pentest recon, a CTF is a single application with intentionally planted clues, so recon should finish within 2-3 rounds. Covers source code leaks, backup files, hidden paths, and clue extraction from page content"
zh-signals: "CTF Web 挑战专用侦察方法，用于在 2-3 轮内发现源码泄露、备份文件、隐藏路径与页面线索。信号:CTF,侦察,源码泄露,备份文件,信息收集"
when-to-use: "Use when facing a CTF web target and needing to quickly discover attack entry points such as source leaks, backup files, hidden paths, or clues in page content."
metadata:
  tags: "ctf,recon,source-leak,backup-file,robots,git,web,enumeration"
  category: "ctf"
---

# CTF Web Recon Methodology

CTF recon is fundamentally different from real-world pentest recon:
- Real-world pentest: many assets, requires subdomain enumeration, port scanning, and fingerprinting
- CTF: **a single web application where the challenge author intentionally left clues**, and the goal of recon is to find those clues

Core principle: **finish recon within 2-3 rounds**; do not spend too many rounds on recon.

## Phase 1: Recon Workflow

### 1.1 Homepage Analysis

Use `http_request` to GET the homepage and inspect the response carefully:

### HTTP Response Headers
- `Server` — server type and version (Apache/Nginx/Express)
- `X-Powered-By` — backend language (PHP/Express/ASP.NET)
- `Set-Cookie` — cookie format (PHPSESSID=PHP, connect.sid=Node, JSESSIONID=Java)
- Non-standard headers — the challenge author may drop hints through custom headers

### HTML Content
- `<!-- comments -->` — CTF authors frequently leave hints in comments (passwords, paths, vulnerability types)
- `<input type="hidden">` — hidden fields may be tampered with
- `<form action="...">` — the form submission target exposes a backend endpoint
- `<script src="...">` — JS file paths expose the project structure
- Page text — sometimes the hint is right in the page content ("Try harder", "Look deeper")

### 1.2 Critical Path Checks

Check in priority order (analyze as soon as you find something; do not mechanically check everything):

### Information Leak Paths
```
/robots.txt          — most common hint location; Disallow paths are often the key ones
/.git/HEAD           — Git source leak (if present, recover the full repo with githacker --brute, including stash/all branches)
/.svn/entries        — SVN leak
/.DS_Store           — macOS directory listing leak
/crossdomain.xml     — Flash cross-domain policy (may expose internal domains)
/.env                — environment variable file (database passwords, API keys)
/composer.json       — PHP dependencies (exposes framework version)
/package.json        — Node.js dependencies
```

### Backup Files
```
/www.zip, /www.tar.gz, /backup.zip     — full site archives
/index.php.bak, /index.php~, /index.php.swp  — editor backups
/flag.txt, /flag, /flag.php             — read the flag directly (sometimes it really is that simple)
/.index.php.swp                         — Vim swap file
```

### Administrative Entry Points
```
/admin, /admin.php, /login, /login.php
/console, /dashboard, /phpmyadmin
/api, /api/v1, /graphql
```

### 1.3 JavaScript Analysis

If the homepage references JS files, fetch them with `http_request` and search for:

- API endpoint paths (`/api/`, `fetch(`, `axios.`)
- Hardcoded credentials (`password`, `token`, `secret`, `key`)
- Hidden functionality (`admin`, `debug`, `test`)
- Hints inside comments

**Tip**: minified/obfuscated JS does not need to be fully understood; just search for key strings.

### 1.4 Technology Stack Confirmation

Confirm the technology stack from the information gathered above, since it determines the direction of the subsequent exploitation:

| Indicator | Tech stack | Common vulnerabilities |
|------|--------|----------|
| `.php` suffix, PHPSESSID | PHP | LFI, deserialization, file upload |
| `express`, connect.sid | Node.js | prototype pollution, SSTI (EJS) |
| JSESSIONID, `.jsp` | Java | deserialization, JNDI, SpEL |
| `_csrf_token`, `csrfmiddlewaretoken` | Python Django | SSTI (Jinja2) |
| `session=eyJ` | Python Flask | Flask session forgery |

## Phase 2: Recon Supplements

### 2.1 What Not to Do
- ❌ Do not run subdomain enumeration against a CTF target (there is only one application)
- ❌ Do not run large-scale port scanning (usually only one port is open)
- ❌ Do not spend more than 3 rounds on recon (the clue is either in recon or in a functional area)

### 2.2 Technology Fingerprinting
- NoSQL/MongoDB indicators: try NoSQL injection operators such as `$gt` and `$ne`

### 2.3 CTF Efficiency
- Single CTF application: no subdomain enumeration, no large-scale port scanning
