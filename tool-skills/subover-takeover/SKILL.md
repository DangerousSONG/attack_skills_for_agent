---
name: subover-takeover
description: 渗透工具 skill:SubOver 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 SubOver 时使用。
---

# SubOver

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/Ice3man543/SubOver
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/Ice3man543/SubOver@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `subover -l subs.txt` | 子域接管检测 |
| `-l file -t 50` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 子域接管批扫

```bash
subover -l all_subs.txt
# dangling CNAME 检测
```

## 注意事项

快速子域接管检测,20+ 服务商指纹。
