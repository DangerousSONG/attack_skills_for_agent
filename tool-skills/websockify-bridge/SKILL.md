---
name: websockify-bridge
description: "websockify: WebSocket tunnel encapsulation for C2/remote control traffic. Signals: covert callback, communication channel, force SSL, TLS certificate, keepalive."
zh-signals: "websockify: WebSocket 隧道封装 C2/远控流量。信号:隐蔽回连,通信通道,强制 SSL,TLS 证书,保活。"
when-to-use: >-
  Use when you need a covert callback or remote-control channel and want to wrap arbitrary TCP
  traffic such as RDP or VNC inside a WebSocket or WSS connection.
---

# websockify

- Attack Category: C36 Covert Callback and Communication Channels
- Upstream Repository: https://github.com/novnc/websockify
- Upstream License: LGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install websockify
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `websockify 127.0.0.1:6080 10.0.0.5:3389` | WebSocket→TCP bridge |
| `--ssl-only` | Force SSL |
| `--cert cert.pem --key key.pem` | TLS certificate |
| `8080 --heartbeat=30` | Keepalive |

## Attack Scenario Playbook

### WebSocket tunnel encapsulation for C2/remote control traffic

```bash
websockify --ssl-only --cert cert.pem --key key.pem 443 127.0.0.1:5900
# The front end uses standard wss:// traffic, blending into normal WebSocket business to evade signature detection
```

## Notes

Wraps arbitrary TCP traffic into WebSocket; a building block for covert channels behind CDNs and web environments.
