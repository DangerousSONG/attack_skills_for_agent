---
name: wpprobe-wp-version
description: wpprobe: WP 组件批量探测。信号:web漏洞,注入,WP 版本+插件探测,插件文件。
---

# wpprobe

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Chocapikk/wpprobe
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install wpprobe
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `wpprobe -u https://t.com` | WP 版本+插件探测 |
| `-u url -f plugins.txt` | 插件文件 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### WP 组件批量探测

```bash
wpprobe -u https://t.com -f plugins.txt
# 基于 readme/version 指纹
```

## 注意事项

轻量 WP 探测器,支持插件级版本识别。
