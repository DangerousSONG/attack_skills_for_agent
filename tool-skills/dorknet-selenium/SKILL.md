---
name: dorknet-selenium
description: 渗透工具 skill:DorkNet 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 DorkNet 时使用。
---

# DorkNet

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/NullArray/DorkNet
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NullArray/DorkNet && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python DorkNet.py -d 'inurl:admin.php' -l results.txt` | Selenium 跑 dork |
| `-d dork -v` | 详细 |
| `-o` | 仅输出 URL |

## 攻击场景 Playbook

### 反爬场景 dork

```bash
python DorkNet.py -d 'site:t.com ext:log'
# Selenium 驱动,绕 Google 简单反爬
```

## 注意事项

Selenium 驱动的 dork 工具,适合传统 HTTP 请求被拦的场景。
