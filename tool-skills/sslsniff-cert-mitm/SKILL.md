---
name: sslsniff-cert-mitm
description: "sslsniff performs SSL MITM. Signals: MITM, mitm, SSL MITM, specify certificate"
zh-signals: "sslsniff: SSL 中间人。信号:中间人,mitm,SSL MITM,指定证书。"
---

# sslsniff

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/moxie0/sslsniff
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install sslsniff
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sslsniff -a -w /tmp/log -p 443` | SSL MITM |
| `-c cert.pem -k key.pem` | 指定证书 |

## 攻击场景 Playbook

### SSL 中间人

```bash
sslsniff -a -c fake.pem -k fake.key -w certs/
# 配合 ARP 毒化
```

## 注意事项

Moxie Marlinspike 出品 SSL MITM 工具。
