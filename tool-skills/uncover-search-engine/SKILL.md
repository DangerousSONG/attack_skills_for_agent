---
name: uncover-search-engine
description: "uncover: Multi-engine asset aggregation search. Signals: network topology, internet mapping, single query, batch query, specified engines."
zh-signals: "uncover: 多引擎资产聚合搜索。信号:网络拓扑,互联网测绘,单查询,批量查询,指定引擎。"
---

# uncover

- 攻击大类:C04 网络拓扑与互联网测绘
- 上游仓库:https://github.com/projectdiscovery/uncover
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/uncover/cmd/uncover@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-q 'search query'` | 单查询 |
| `-q query.txt` | 批量查询 |
| `-e shodan,censys,fofa,quake,zoomeye` | 指定引擎 |
| `-ue` | 用户引擎 ~/.config/uncover/provider-config.yaml |
| `-o out.txt` | 输出 |
| `-l 100` | 限制条数 |

## 攻击场景 Playbook

### 多引擎资产聚合搜索

```bash
uncover -q 'org:"Target Corp" http.title:"login"' -e shodan,censys -l 200
fofa 语法: uncover -q 'domain="corp.com"' -e fofa -l 500
```

## 注意事项

pd 生态聚合器,一个 CLI 调 Shodan/Censys/Fofa/Quake/ZoomEye/Hunter;API key 配 provider-config.yaml。
