---
name: machinae-osint
description: 渗透工具 skill:machinae 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 machinae 时使用。
when-to-use: 渗透工具 skill:machinae 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 machinae 时使用。
---

# machinae

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/HurricaneLabs/machinae
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install machinae
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `machinae target.com` | 多源 OSINT 查询 |
| `-s shodan,censys` | 指定源 |
| `-f sites.txt` | 批量 |
| `-o out.json` | JSON 输出 |

## 攻击场景 Playbook

### 域名/IP/邮箱多源情报

```bash
machinae corp.com
# Shodan/Censys/VirusTotal 等 20+ 源一次查
```

## 注意事项

Hurricane Labs 出品,OSINT 情报聚合 CLI。
