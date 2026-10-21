---
name: ropeadope-logclean
description: 渗透工具 skill:ropeadope 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 ropeadope 时使用。
when-to-use: 渗透工具 skill:ropeadope 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 ropeadope 时使用。
---

# ropeadope

- 攻击大类:C20 反取证与痕迹清理
- 上游仓库:https://github.com/BullsEye0/ropeadope
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/BullsEye0/ropeadope && chmod +x ropeadope.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./ropeadope.sh` | 交互式 Linux 日志清理 |
| `--wtmp` | 清登录记录 |
| `--auth` | 清认证日志 |
| `--shell` | 清 shell history |

## 攻击场景 Playbook

### Linux 主机日志清理

```bash
./ropeadope.sh  # 按菜单清 wtmp/btmp/auth.log/lastlog/shell history
```

## 注意事项

脚本型工具需 root;清日志是高度敏感操作,授权演练中先快照留证再执行。
