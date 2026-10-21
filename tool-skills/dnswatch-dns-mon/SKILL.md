---
name: dnswatch-dns-mon
description: 渗透工具 skill:DNSWatch 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 DNSWatch 时使用。
when-to-use: 渗透工具 skill:DNSWatch 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 DNSWatch 时使用。
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
