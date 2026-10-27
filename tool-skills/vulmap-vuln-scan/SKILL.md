---
name: vulmap-vuln-scan
description: Vulmap: 本地 CVE 一键扫。信号:漏洞情报,cve,本地漏洞扫描,更新漏洞库,指定应用。
---

# Vulmap

- 攻击大类:C06 漏洞情报与漏洞库
- 上游仓库:https://github.com/vulmon/Vulmap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/vulmon/Vulmap && cd Vulmap/Unix && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 vulmap.py` | 本地漏洞扫描 |
| `-u` | 更新漏洞库 |
| `-a apache,nginx` | 指定应用 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 本地 CVE 一键扫

```bash
python3 vulmap.py
# 系统+中间件 CVE 匹配
```

## 注意事项

Vulmon 出品本地漏洞扫描器。
