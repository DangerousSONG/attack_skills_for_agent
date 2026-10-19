---
name: crypthook-encrypted-tunnel
description: 渗透工具 skill:CryptHook 的安装、参数速查与攻击场景 playbook。当任务涉及 隧道与代理 需要调用 CryptHook 时使用。
---

# CryptHook

- 攻击大类:C32 隧道与代理
- 上游仓库:https://github.com/chokepoint/CryptHook
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/chokepoint/CryptHook && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./crypthook -k presharedkey -l 4444` | 加密监听 |
| `./crypthook -k key -c target.com -p 443` | 加密连接 |
| `iptables 转发到目标` | 结合使用 |
| `-d` | daemon 模式 |

## 攻击场景 Playbook

### 加密隧道转发任意 TCP

```bash
./crypthook -k secret -l 4444  # 服务端
./crypthook -k secret -c 10.0.0.5 -p 4444  # 客户端
# AES 加密 TCP 转发,IDS 看到的是密文
```

## 注意事项

点对点 AES 加密 TCP 隧道,轻量单文件,适合嵌套在现有代理链中加密一层。
