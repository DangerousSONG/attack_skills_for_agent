---
name: pagodo-dorks
description: 渗透工具 skill:pagodo 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 pagodo 时使用。
---

# pagodo

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/opsdisk/pagodo
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/opsdisk/pagodo && cd pagodo && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python pagodo.py -d target.com -g dorks.txt` | 跑 GHDB dork 集 |
| `-l` | 限速 |
| `-j 20` | 并发 |

## 攻击场景 Playbook

### GHDB 漏洞指纹 dork 批跑

```bash
python pagodo.py -d corp.com -g ~/pagodo/all_google_dorks.txt -j 10
# 对目标跑 4000+ 条漏洞/泄露 dork,结果即潜在 findings
```

## 注意事项

内置整个 Google Hacking Database;结果可直接当漏洞线索清单。
