---
name: uptux-linux-check
description: "uptux: Linux systemd privilege escalation detection. Signals: linux privilege escalation, SUID, Linux privilege escalation check, full check, verbose."
zh-signals: "uptux: Linux systemd 提权检测。信号:linux提权,suid,Linux 提权检查,全检查,详细。"
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
