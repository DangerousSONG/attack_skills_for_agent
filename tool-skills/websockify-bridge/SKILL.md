---
name: websockify-bridge
description: websockify: WebSocket 隧道封装 C2/远控流量。信号:隐蔽回连,通信通道,强制 SSL,TLS 证书,保活。
---

# websockify

- 攻击大类:C36 隐蔽回连与通信通道
- 上游仓库:https://github.com/novnc/websockify
- 上游 License:LGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install websockify
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `websockify 127.0.0.1:6080 10.0.0.5:3389` | WebSocket→TCP 桥 |
| `--ssl-only` | 强制 SSL |
| `--cert cert.pem --key key.pem` | TLS 证书 |
| `8080 --heartbeat=30` | 保活 |

## 攻击场景 Playbook

### WebSocket 隧道封装 C2/远控流量

```bash
websockify --ssl-only --cert cert.pem --key key.pem 443 127.0.0.1:5900
# 前端走标准 wss:// 流量,混在正常 WebSocket 业务里难被特征识别
```

## 注意事项

把任意 TCP 流量封装成 WebSocket;CDN/Web 环境做隐蔽通道的底件。
