---
name: sslscan-tls-check
description: "sslscan audits weak TLS configurations. Signals: cryptographic attack, cryptographic cracking, TLS configuration audit, certificate details, skip cipher enumeration"
zh-signals: "sslscan: TLS 弱配置审计。信号:密码学攻击,加密破解,TLS 配置审计,证书详情,跳过套件枚举。"
---

# sslscan

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/rbsec/sslscan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install sslscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sslscan t.com:443` | TLS 配置审计 |
| `--show-certificate` | 证书详情 |
| `--no-ciphersuites` | 跳过套件枚举 |
| `--xml=out.xml` | XML 输出 |

## 攻击场景 Playbook

### TLS 弱配置审计

```bash
sslscan --show-certificate t.com:443
# 弱套件/协议版本/证书问题
```

## 注意事项

TLS/SSL 配置审计,识别弱密码套件和过期协议。
