---
name: kickthemout-deauth
description: "kickthemout kicks LAN devices offline with ARP. Signals: MITM, mitm, LAN device disconnection, kick all."
zh-signals: "kickthemout: 内网设备 ARP 踢下线。信号:中间人,mitm,局域网设备踢下线,kick 全部。"
---

# kickthemout

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/k4m4/kickthemout
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/k4m4/kickthemout && cd kickthemout && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 kickthemout.py` | 局域网设备踢下线 |
| `-s` | 扫描 |
| `-k` | kick 全部 |

## 攻击场景 Playbook

### 内网设备 ARP 踢下线

```bash
python3 kickthemout.py
# 迫使重连钓鱼热点
```

## 注意事项

ARP 欺骗踢设备下线。
