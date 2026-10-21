---
name: gh-dork-github
description: 渗透工具 skill:gh-dork 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 gh-dork 时使用。
when-to-use: 渗透工具 skill:gh-dork 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 gh-dork 时使用。
---

# gh-dork

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/micha3lb3/gh-dork
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/micha3lb3/gh-dork && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 gh-dork.py -u targetcorp` | 组织仓库 dork |
| `-u org -d dorks.txt` | 自定义 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### 组织敏感文件 dork

```bash
python3 gh-dork.py -u corp
# password/env/key 文件名搜索
```

## 注意事项

Github 组织仓库敏感文件搜索。
