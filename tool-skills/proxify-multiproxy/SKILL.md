---
name: proxify-multiproxy
description: proxify: 多协议代理转发。信号:内网穿透,隧道,起多级代理,SOCKS5,流量落盘。
---

# proxify

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/projectdiscovery/proxify
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/proxify@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `proxify -http-addr 0.0.0.0:8888` | 起多级代理 |
| `-socks5-addr 0.0.0.0:9050` | SOCKS5 |
| `-output out/` | 流量落盘 |

## 攻击场景 Playbook

### 多协议代理转发

```bash
proxify -http-addr 127.0.0.1:8080
# HTTP/SOCKS5 互转+TLS 拦截
```

## 注意事项

ProjectDiscovery 出品,多功能代理工具。
