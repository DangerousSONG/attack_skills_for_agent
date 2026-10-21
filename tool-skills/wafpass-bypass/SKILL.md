---
name: wafpass-bypass
description: 渗透工具 skill:WAFPass 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 WAFPass 时使用。
when-to-use: 渗透工具 skill:WAFPass 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 WAFPass 时使用。
---

# WAFPass

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/wafpassproject/wafpass
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/wafpassproject/wafpass
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wafpass.py -u 'https://t.com/?id=1' -vuln sqli` | WAF 绕过测试 |
| `-u url -vuln xss` | XSS 绕过 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 编码混淆绕过 WAF

```bash
python wafpass.py -u 'https://t.com/?id=1' -vuln sqli
# 多种编码/注释混淆组合尝试
```

## 注意事项

WAF 绕过测试工具,多技术混淆组合。
