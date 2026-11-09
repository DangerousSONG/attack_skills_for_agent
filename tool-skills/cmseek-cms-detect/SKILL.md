---
name: cmseek-cms-detect
description: "CMSeeK: Identifies CMS fingerprints and detects deep links. Signals: web vulnerability, injection, CMS identification plus vulnerability detection, follow redirects, rescan."
zh-signals: "CMSeeK: CMS 指纹识别+深链检测。信号:web漏洞,注入,CMS 识别+漏洞检测,跟踪重定向,重扫。"
---

# CMSeeK

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Tuhinshubhra/CMSeeK
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK && cd CMSeeK && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cmseek.py -u https://t.com` | CMS 识别+漏洞检测 |
| `--follow-redirect` | 跟踪重定向 |
| `-r` | 重扫 |
| `--batch` | 批量模式 |
| `--user-agent Mozilla/5.0` | 自定义 UA |

## 攻击场景 Playbook

### CMS 指纹识别+深链检测

```bash
python cmseek.py -u https://t.com
# 识别 170+ 种 CMS,自动跑对应漏洞检测模块
```

## 注意事项

CMS 检测+深度扫描一体,检测到 WordPress/Joomla 等自动转入对应检测流程。
