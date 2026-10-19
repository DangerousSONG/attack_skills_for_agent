---
name: sniffjoke-traffic-obf
description: 渗透工具 skill:sniffjoke 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 sniffjoke 时使用。
---

# sniffjoke

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/vecna/sniffjoke
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install sniffjoke
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sniffjoke -r` | 透明混淆 |
| `-d` | 调试 |
| `-q` | 静默 |

## 攻击场景 Playbook

### 反嗅探流量混淆

```bash
sniffjoke
# 让 IDS/嗅探器解析失败
```

## 注意事项

网络流量混淆,对抗被动嗅探。
