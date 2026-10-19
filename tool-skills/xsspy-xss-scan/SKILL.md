---
name: xsspy-xss-scan
description: 渗透工具 skill:XssPy 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(XSS) 需要调用 XssPy 时使用。
---

# XssPy

- 攻击大类:C09 Web利用(XSS)
- 上游仓库:https://github.com/faizann24/XssPy
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/faizann24/XssPy && pip install mechanize
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python XssPy.py -u https://t.com` | 爬全站扫 XSS |
| `-u url -w wordlist.txt` | 自定义 payload |
| `-s` | 跳过子域 |

## 攻击场景 Playbook

### 整站 XSS 初筛

```bash
python XssPy.py -u https://t.com
# 对发现的每个表单/参数注入 payload 并检测回显
```

## 注意事项

Python2 时代老工具,胜在简单粗暴整站爬;精细验证建议再上 Dalfox(现有)。
