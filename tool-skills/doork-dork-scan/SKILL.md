---
name: doork-dork-scan
description: 渗透工具 skill:doork 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 doork 时使用。
when-to-use: 渗透工具 skill:doork 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 doork 时使用。
---

# doork

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/AeonDave/doork
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/AeonDave/doork && cd doork
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python doork.py -t corp.com` | Google dork 目标扫描 |
| `-t target -g 'ext:sql'` | 自定义 dork |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 目标 dork 自动化

```bash
python doork.py -t corp.com
# 泄露文件/后台/配置自动 dork
```

## 注意事项

Google dork 自动化,预置敏感文件类型查询。
