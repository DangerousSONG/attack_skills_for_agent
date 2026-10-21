---
name: vbscan-vbulletin
description: 渗透工具 skill:VBScan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 VBScan 时使用。
when-to-use: 渗透工具 skill:VBScan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 VBScan 时使用。
---

# VBScan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/rezasp/vbscan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/rezasp/vbscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `perl vbscan.pl https://t.com/forum` | vBulletin 扫描 |
| `--cookies 'x=1'` | 带 Cookie |
| `-o` | 输出报告 |

## 攻击场景 Playbook

### vBulletin 漏洞扫描

```bash
perl vbscan.pl https://t.com/forum
# 版本/组件/漏洞库比对
```

## 注意事项

vBulletin 论坛专项扫描器。
