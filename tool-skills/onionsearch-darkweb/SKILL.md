---
name: onionsearch-darkweb
description: "Multi-engine dark web intelligence aggregation. Signals: web vulnerability, injection, multi dark-web engine search, pages, specified engines."
zh-signals: "OnionSearch: 多引擎暗网情报聚合。信号:web漏洞,注入,多暗网引擎搜索,页数,指定引擎。"
---

# OnionSearch

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/megadose/OnionSearch
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install onionsearch
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `onionsearch 'target'` | 多暗网引擎搜索 |
| `-p 5` | 页数 |
| `--engines ahmia,tor66` | 指定引擎 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 多引擎暗网情报聚合

```bash
onionsearch 'corp.com'
# ahmia/tor66 等 8+ 暗网引擎一次查
```

## 注意事项

megadose 出品,聚合多个暗网搜索引擎,目标威胁情报收集。
