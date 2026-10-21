---
name: atscan-web-scan
description: 渗透工具 skill:ATSCAN 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 ATSCAN 时使用。
when-to-use: 渗透工具 skill:ATSCAN 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 ATSCAN 时使用。
---

# ATSCAN

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/AlisamTechnology/ATSCAN-V3.1
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/AlisamTechnology/ATSCAN-V3.1
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `perl atscan.pl -d 'dork' -l 10` | dork 扫描 |
| `--target t.com -s` | XSS/SQLi 扫描 |
| `-t 10` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### dork+漏洞双引擎

```bash
perl atscan.pl -d 'inurl:php?id=' -l 20
# 搜索引擎+漏洞扫描一体
```

## 注意事项

Perl 多引擎扫描器,dork/端口/XSS/SQLi 一体。
