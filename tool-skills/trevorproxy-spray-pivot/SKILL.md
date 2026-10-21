---
name: trevorproxy-spray-pivot
description: 渗透工具 skill:TREVORproxy 的安装、参数速查与攻击场景 playbook。当任务涉及 隧道与内网穿透 需要调用 TREVORproxy 时使用。
when-to-use: 渗透工具 skill:TREVORproxy 的安装、参数速查与攻击场景 playbook。当任务涉及 隧道与内网穿透 需要调用 TREVORproxy 时使用。
---

# TREVORproxy

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/blacklanternsecurity/TREVORproxy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install trevorproxy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `trevorproxy -i eth0 -d target.com` | 代理池喷洒 |
| `-i eth0 -d d -u u.txt` | 组合 |
| `-l` | 列表 |

## 攻击场景 Playbook

### 多源 IP 喷洒

```bash
trevorproxy -i eth0 -d corp.com
# 多网卡 IP 轮换
```

## 注意事项

Black Lantern 出品,多出口 IP 代理。
