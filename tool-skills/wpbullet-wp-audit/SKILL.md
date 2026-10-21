---
name: wpbullet-wp-audit
description: 渗透工具 skill:wpbullet 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 wpbullet 时使用。
when-to-use: 渗透工具 skill:wpbullet 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 wpbullet 时使用。
---

# wpbullet

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/webarx-security/wpbullet
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/webarx-security/wpbullet && cd wpbullet && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wpbullet.py -u https://t.com` | WP 漏洞扫描 |
| `-u url --aggressive` | 激进模式 |
| `-u url -e vp` | 仅插件 |

## 攻击场景 Playbook

### WP 插件漏洞扫描

```bash
python wpbullet.py -u https://t.com
# 50+ 插件漏洞 PoC
```

## 注意事项

WebARX 出品的 WP 扫描器,插件漏洞库精。
