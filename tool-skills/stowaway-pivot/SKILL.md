---
name: stowaway-pivot
description: "Stowaway provides multi-layer internal network pivoting. Signals: internal pivoting, tunneling, agent listen, admin connection, key"
zh-signals: "Stowaway: 多层内网穿透。信号:内网穿透,隧道,agent 监听,admin 连接,密钥。"
---

# Stowaway

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/ph4ntonn/Stowaway
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ph4ntonn/Stowaway && cd Stowaway && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./stowaway_agent -l 9999` | agent 监听 |
| `./stowaway_admin -c 10.0.0.5:9999` | admin 连接 |
| `-s secret` | 密钥 |
| `socks 5` | SOCKS 代理 |

## 攻击场景 Playbook

### 多层内网穿透

```bash
./stowaway_agent -l 9999 && ./stowaway_admin -c target:9999
# 多级 agent 拓扑
```

## 注意事项

Go 内网穿透框架,多级 agent+SOCKS5。
