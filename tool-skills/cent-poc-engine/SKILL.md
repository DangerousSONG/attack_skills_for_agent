---
name: cent-poc-engine
description: cent: nuclei 模板一键扩容。信号:web漏洞,注入,按关键字筛选模板,指定输出目录,排除模板。
---

# cent

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/xm1k3/cent
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/xm1k3/cent@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cent -p` | 拉取全部社区 nuclei 模板 |
| `cent -p -k 'cve-2023'` | 按关键字筛选模板 |
| `cent -p -o ~/nuclei-templates` | 指定输出目录 |
| `-e id1,id2` | 排除模板 |

## 攻击场景 Playbook

### nuclei 模板一键扩容

```bash
cent -p && nuclei -u https://t.com -t ~/cent-nuclei-templates
# 社区模板集大成,漏洞覆盖直接翻倍
```

## 注意事项

nuclei 模板聚合引擎,自动从数十个社区仓库拉取模板,是 nuclei(现有) 的模板补充器。
