---
name: dirstalk-dir-scan
description: 渗透工具 skill:dirstalk 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 dirstalk 时使用。
---

# dirstalk

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/stefanoj3/dirstalk
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/stefanoj3/dirstalk@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dirstalk scan https://t.com -d wordlist.txt` | 目录扫描 |
| `-d w.txt -t 30` | 线程 |
| `-s status_codes=200,301` | 状态过滤 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 分布式目录扫描

```bash
dirstalk scan https://t.com -d raft-medium.txt
# 支持分布式 agent
```

## 注意事项

Go 目录扫描,支持分布式扫描。
