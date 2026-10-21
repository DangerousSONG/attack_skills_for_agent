---
name: uptux-linux-check
description: 渗透工具 skill:uptux 的安装、参数速查与攻击场景 playbook。当任务涉及 Linux本地提权 需要调用 uptux 时使用。
when-to-use: 渗透工具 skill:uptux 的安装、参数速查与攻击场景 playbook。当任务涉及 Linux本地提权 需要调用 uptux 时使用。
---

# uptux

- 攻击大类:C16 Linux本地提权
- 上游仓库:https://github.com/initstring/uptux
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/initstring/uptux
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 uptux.py` | Linux 提权检查 |
| `-a` | 全检查 |
| `-d` | 详细 |

## 攻击场景 Playbook

### Linux systemd 提权检测

```bash
python3 uptux.py
# systemd 配置/定时器/socket 提权
```

## 注意事项

聚焦 systemd 的 Linux 提权枚举。
