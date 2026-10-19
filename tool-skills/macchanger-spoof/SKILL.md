---
name: macchanger-spoof
description: 渗透工具 skill:macchanger 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 macchanger 时使用。
---

# macchanger

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/alobbs/macchanger
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install macchanger
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `macchanger -r eth0` | 随机 MAC |
| `-m 00:11:22:33:44:55` | 指定 MAC |
| `-s eth0` | 查看 |

## 攻击场景 Playbook

### MAC 地址伪装

```bash
macchanger -r wlan0
# 绕过 MAC 过滤
```

## 注意事项

MAC 地址修改工具。
