---
name: sippts-sip-attack
description: 渗透工具 skill:sippts 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 sippts 时使用。
when-to-use: 渗透工具 skill:sippts 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 sippts 时使用。
---

# sippts

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/Pepelux/sippts
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Pepelux/sippts && cd sippts
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./sippts scan -i 10.0.0.0/24` | SIP 扫描 |
| `extenum -i ip -e 100-999` | 分机枚举 |
| `crack -i ip -u 100 -w pass.txt` | SIP 爆破 |
| `spoof -i ip` | CallerID 伪造 |

## 攻击场景 Playbook

### VoIP 内网攻击

```bash
./sippts scan -i 10.0.0.0/24 && ./sippts extenum -i 10.0.0.5
# 发现+枚举+爆破
```

## 注意事项

Pepelux 出品 SIP 工具集。
