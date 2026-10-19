---
name: jaeles-vuln-scan
description: 渗透工具 skill:jaeles 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 jaeles 时使用。
---

# jaeles

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/jaeles-project/jaeles
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/jaeles-project/jaeles@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `jaeles scan -u https://t.com` | 内置签名扫描 |
| `-x 'sqli,xxe'` | 指定签名族 |
| `jaeles config add -R ~/custom-signatures` | 自定义签名 |
| `-o out/` | 输出 |
| `--proxy http://127.0.0.1:8080` | 过 Burp |

## 攻击场景 Playbook

### 签名驱动漏洞验证

```bash
jaeles scan -u https://t.com -x rce
# YAML 签名,OOB 联动,比 nuclei 更灵活的结果判定
```

## 注意事项

签名化漏洞扫描框架,YAML 签名支持多请求链+OOB 关联验证,gospider 同生态。
