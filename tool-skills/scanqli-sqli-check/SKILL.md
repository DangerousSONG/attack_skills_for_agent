---
name: scanqli-sqli-check
description: "ScanQLi: Quickly validates SQL injection. Signals: web vulnerabilities, injection, SQLi scanning, database enumeration, threads."
zh-signals: "ScanQLi: SQLi 快速验证。信号:web漏洞,注入,SQLi 扫描,库枚举,线程。"
---

# ScanQLi

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/bambish/ScanQLi
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bambish/ScanQLi && cd ScanQLi
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 scanqli.py -u 'https://t.com/?id=1'` | SQLi 扫描 |
| `-u url --dbs` | 库枚举 |
| `-t 10` | 线程 |

## 攻击场景 Playbook

### SQLi 快速验证

```bash
python3 scanqli.py -u 'https://t.com/item?id=5'
# 错误/时间盲注双模式
```

## 注意事项

轻量 SQLi 扫描器,支持批量 URL。
