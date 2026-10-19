---
name: botb-container-attack
description: 渗透工具 skill:botb (Break Out The Box) 的安装、参数速查与攻击场景 playbook。当任务涉及 云与容器执行 需要调用 botb (Break Out The Box) 时使用。
---

# botb (Break Out The Box)

- 攻击大类:C14 云与容器执行
- 上游仓库:https://github.com/brompwnie/botb
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/brompwnie/botb@latest 或 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `botb -analyze` | 静态容器分析 |
| `-socketpath /var/run/docker.sock` | 指定 socket |
| `-recon` | 仅枚举 |
| `-exploit` | 执行逃逸 |
| `-findDockerd` | 找 dockerd |

## 攻击场景 Playbook

### 容器评估+逃逸一体

```bash
botb -analyze  # 输出: capabilities/挂载/env secret/逃逸可行性评分
botb -analyze -exploit
```

## 注意事项

Go 单文件方便投递进容器;与 deepce 互补(botb 偏静态分析)。
