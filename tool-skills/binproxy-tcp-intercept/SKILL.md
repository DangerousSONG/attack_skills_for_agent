---
name: binproxy-tcp-intercept
description: 渗透工具 skill:BinProxy 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 BinProxy 时使用。
---

# BinProxy

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/nccgroup/BinProxy
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install binproxy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `binproxy -l 8080 -r 10.0.0.5:3389 -p rdp` | 二进制协议中间人 |
| `-l l -r r -p proto -s` | SSL |
| `-d` | 调试 |

## 攻击场景 Playbook

### 私有协议中间人

```bash
binproxy -l 8080 -r 10.0.0.5:1433 -p tds
# NCC 出品,拦截 RDP/MSSQL 等
```

## 注意事项

NCC 出品,任意二进制协议中间人代理。
