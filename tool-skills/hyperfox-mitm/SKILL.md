---
name: hyperfox-mitm
description: Hyperfox: HTTP 流量中间人分析。信号:中间人,mitm,透明代理,流量落盘。
---

# Hyperfox

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/xiam/hyperfox
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/xiam/hyperfox@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `hyperfox -p 8080 -c cert.pem -k key.pem` | HTTP/HTTPS 中间人 |
| `-p port -s` | 透明代理 |
| `-o out/` | 流量落盘 |

## 攻击场景 Playbook

### HTTP 流量中间人分析

```bash
hyperfox -p 8080 -c fake.crt -k fake.key
# 记录+篡改 HTTP 请求
```

## 注意事项

Go 中间人代理,流量记录+实时篡改。
