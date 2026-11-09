---
name: rbndr-dns-rebinding
description: "rbndr: Bypasses browser same-origin policy. Signals: man-in-the-middle, MITM, DNS rebinding, A records, TTL control."
zh-signals: "rbndr: 浏览器同源策略绕过。信号:中间人,mitm,DNS 重绑定,A 记录,TTL 控制。"
---

# rbndr

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/taviso/rbndr
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/taviso/rbndr && cd rbndr && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./rbndr 10.0.0.5 target.com` | DNS 重绑定 |
| `-a` | A 记录 |
| `-t TTL` | TTL 控制 |

## 攻击场景 Playbook

### 浏览器同源策略绕过

```bash
./rbndr 127.0.0.1 internal.corp.local
# 打内网绕过 SOP
```

## 注意事项

taviso 出品 DNS 重绑定工具。
