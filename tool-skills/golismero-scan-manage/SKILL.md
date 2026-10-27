---
name: golismero-scan-manage
description: Golismero: 带知识库管理的扫描。信号:web漏洞,注入,全自动扫描,HTML 报告,启用插件。
---

# Golismero

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/golismero/golismero
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/golismero/golismero
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python golismero.py scan t.com` | 全自动扫描 |
| `python golismero.py scan t.com -o report.html` | HTML 报告 |
| `-e nikto,nmap` | 启用插件 |
| `-a` | 全部插件 |

## 攻击场景 Playbook

### 带知识库管理的扫描

```bash
python golismero.py scan t.com -o report.html
# 结果自动去重+知识库分类,适合团队协作
```

## 注意事项

开源漏洞管理框架,插件化,自带去重和报告系统。
