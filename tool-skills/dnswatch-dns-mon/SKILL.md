---
name: dnswatch-dns-mon
description: DNSWatch: DNS 请求监控+劫持。信号:中间人,mitm,DNS 监控+伪造,伪造模式,定向。
---

# DNSWatch

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/HalilDeniz/DNSWatch
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/HalilDeniz/DNSWatch && cd DNSWatch && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 dnswatch.py -i eth0` | DNS 监控+伪造 |
| `-i eth0 -f` | 伪造模式 |
| `-i eth0 -d example.com/10.0.0.5` | 定向 |

## 攻击场景 Playbook

### DNS 请求监控+劫持

```bash
python3 dnswatch.py -i eth0
# 内网 DNS 分析+钓鱼重定向
```

## 注意事项

DNS 监控+伪造一体化。
