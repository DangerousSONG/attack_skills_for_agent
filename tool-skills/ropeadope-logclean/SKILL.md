---
name: ropeadope-logclean
description: "ropeadope: Cleans Linux host logs. Signals: trace cleanup, anti-forensics, clear login records, clear authentication logs."
zh-signals: "ropeadope: Linux 主机日志清理。信号:痕迹清理,反取证,清登录记录,清认证日志。"
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
