---
name: climber-linux-audit
description: 渗透工具 skill:climber 的安装、参数速查与攻击场景 playbook。当任务涉及 Linux本地提权 需要调用 climber 时使用。
---

# climber

- 攻击大类:C16 Linux本地提权
- 上游仓库:https://github.com/raffaele-forte/climber
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/raffaele-forte/climber
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bash climber.sh` | Linux 系统审计 |
| `-s` | 服务检查 |
| `-u` | 用户权限 |

## 攻击场景 Playbook

### Linux 提权路径枚举

```bash
bash climber.sh
# Suid/cron/内核/服务配置
```

## 注意事项

Linux 提权枚举脚本。
