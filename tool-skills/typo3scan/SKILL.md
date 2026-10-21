---
name: typo3scan
description: 渗透工具 skill:Typo3Scan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Typo3Scan 时使用。
when-to-use: 渗透工具 skill:Typo3Scan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Typo3Scan 时使用。
---

# Typo3Scan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/whoot/Typo3Scan
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/whoot/Typo3Scan && cd Typo3Scan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 typo3scan.py -d t.com` | Typo3 枚举+漏洞扫描 |
| `-d domain -s` | SSL |
| `-o out.txt` | 输出 |
| `-f domains.txt` | 批量 |

## 攻击场景 Playbook

### Typo3 漏洞扫描

```bash
python3 typo3scan.py -d t.com
# 扩展/版本/CVE 全检测
```

## 注意事项

Typo3 CMS 专项扫描,扩展级漏洞库。
