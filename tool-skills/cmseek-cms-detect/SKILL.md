---
name: cmseek-cms-detect
description: 渗透工具 skill:CMSeeK 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 CMSeeK 时使用。
when-to-use: 渗透工具 skill:CMSeeK 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 CMSeeK 时使用。
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
