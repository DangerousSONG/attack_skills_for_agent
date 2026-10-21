---
name: bridgekeeper-username-mangle
description: 渗透工具 skill:BridgeKeeper 的安装、参数速查与攻击场景 playbook。当任务涉及 OSINT情报收集 需要调用 BridgeKeeper 时使用。
when-to-use: 渗透工具 skill:BridgeKeeper 的安装、参数速查与攻击场景 playbook。当任务涉及 OSINT情报收集 需要调用 BridgeKeeper 时使用。
---

# BridgeKeeper

- 攻击大类:C03 OSINT情报收集
- 上游仓库:https://github.com/0xZDH/BridgeKeeper
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xZDH/BridgeKeeper && cd BridgeKeeper
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python bridgekeeper.py -f names.txt -d corp.com` | 人名→用户名规则生成 |
| `-f names.txt -d corp.com --format first.last` | 指定格式 |
| `-o users.txt` | 输出 |
| `--formats` | 列出所有规则 |

## 攻击场景 Playbook

### HR 名单变喷洒字典

```bash
python bridgekeeper.py -f employees.txt -d corp.com -o users.txt
# John Smith→john.smith/jsmith/j.smith 全变体
```

## 注意事项

OSINT 拿到员工名单后按企业命名惯例生成用户名,喷洒/爆破的前置工具。
