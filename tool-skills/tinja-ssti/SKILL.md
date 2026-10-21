---
name: tinja-ssti
description: 渗透工具 skill:TInjA 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 TInjA 时使用。
when-to-use: 渗透工具 skill:TInjA 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 TInjA 时使用。
---

# TInjA

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Hackmanit/TInjA
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/Hackmanit/TInjA@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `tinja -u 'https://t.com/?name=x' -ac 'error'` | SSTI 检测 |
| `-u url -H 'Cookie: x'` | 带 Cookie |
| `-r req.txt` | 请求文件 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### SSTI 全引擎检测

```bash
tinja -u 'https://t.com/greet?name=admin' -ac 'syntax error'
# 探测 30+ 模板引擎,出可利用 payload
```

## 注意事项

Hackmanit 出品的 SSTI 扫描器,支持 cannibalization 模式深挖。
