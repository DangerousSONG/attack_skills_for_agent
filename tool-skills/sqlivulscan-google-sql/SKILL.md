---
name: sqlivulscan-google-sql
description: 渗透工具 skill:sqlivulscan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 sqlivulscan 时使用。
---

# sqlivulscan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/Hadesy2k/sqlivulscan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Hadesy2k/sqlivulscan && cd sqlivulscan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python sqlivulscan.py -d 'inurl:php?id='` | Google dork 找 SQLi |
| `-t 'http://t.com/?id=1'` | 单目标 |
| `-e bing` | 引擎选择 |

## 攻击场景 Playbook

### dork 批量找注入点

```bash
python sqlivulscan.py -d 'inurl:index.php?id='
# 自动采 URL 逐测错误注入
```

## 注意事项

搜索引擎+dork 批量 SQLi 发现。
