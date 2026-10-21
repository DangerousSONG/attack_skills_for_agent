---
name: moonwalk-anti-forensic
description: 渗透工具 skill:moonwalk 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 moonwalk 时使用。
when-to-use: 渗透工具 skill:moonwalk 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 moonwalk 时使用。
---

# moonwalk

- 攻击大类:C20 反取证与痕迹清理
- 上游仓库:https://github.com/mufeedvh/moonwalk
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install moonwalk 或 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `moonwalk start` | 开始记录时间戳基线 |
| `执行操作...` | 活动期 |
| `moonwalk finish` | 恢复全部 mtime/atime |
| `-m` | 内存执行模式 |
| `-d dir` | 限定目录 |

## 攻击场景 Playbook

### Linux 痕迹时间线抹除

```bash
moonwalk start
# 执行渗透操作(文件访问/修改)
moonwalk finish  # 所有时间戳恢复基线,审计时间线断裂
```

## 注意事项

Rust 写的反取证,恢复文件时间线;配合 mat2 清元数据形成完整清理链。
