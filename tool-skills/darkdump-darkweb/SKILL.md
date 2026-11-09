---
name: darkdump-darkweb
description: "darkdump: Searches dark web intelligence. Signals: web vulnerability, injection, dark web search, page count."
zh-signals: "darkdump: 暗网情报搜索。信号:web漏洞,注入,暗网搜索,页数。"
---

# darkdump

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/josh0xA/darkdump
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/josh0xA/darkdump && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 darkdump.py -q 'target corp'` | 暗网搜索 |
| `-q keywords -p 3` | 页数 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 暗网情报搜索

```bash
python3 darkdump.py -q 'corp.com'
# 暗网论坛/市场提及目标的信息泄露线索
```

## 注意事项

暗网(.onion)搜索引擎接口封装,查目标泄露数据/威胁情报。
