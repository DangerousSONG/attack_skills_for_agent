---
name: driftnet-image-sniff
description: "driftnet: LAN image sniffing. Signals: man-in-the-middle, MITM, image traffic sniffing, audio, save to disk."
zh-signals: "driftnet: 局域网图片嗅探。信号:中间人,mitm,图片流量嗅探,音频,落盘。"
---

# driftnet

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/deiv/driftnet
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install driftnet
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `driftnet -i eth0` | 图片流量嗅探 |
| `-a` | 音频 |
| `-d tmp/` | 落盘 |
| `-f` | 前台 |

## 攻击场景 Playbook

### 局域网图片嗅探

```bash
driftnet -i eth0
# ARP 欺骗下看目标浏览图片
```

## 注意事项

网络图片嗅探工具。
