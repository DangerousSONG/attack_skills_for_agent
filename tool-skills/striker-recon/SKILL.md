---
name: striker-recon
description: Striker: 目标快速画像。信号:web漏洞,注入,信息收集+漏洞初判,详细。
---

# Striker

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/UltimateHackers/Striker
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/UltimateHackers/Striker && cd Striker && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python striker.py t.com` | 信息收集+漏洞初判 |
| `-o report` | 输出 |
| `-d` | 详细 |

## 攻击场景 Playbook

### 目标快速画像

```bash
python striker.py t.com
# WAF/云/CDN/子域/端口/常见漏洞一站式
```

## 注意事项

信息收集+漏洞初判一体,输出目标技术栈画像。
