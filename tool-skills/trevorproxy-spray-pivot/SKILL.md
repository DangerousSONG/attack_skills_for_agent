---
name: trevorproxy-spray-pivot
description: "TREVORproxy sprays from multiple source IPs. Signals: internal pivoting, tunneling, proxy-pool spraying, combinations, lists"
zh-signals: "TREVORproxy: 多源 IP 喷洒。信号:内网穿透,隧道,代理池喷洒,组合,列表。"
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
