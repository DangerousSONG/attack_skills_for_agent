---
name: fuzzdb-payload-dict
description: 渗透工具 skill:fuzzdb 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 fuzzdb 时使用。
---

# fuzzdb

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/fuzzdb-project/fuzzdb
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/fuzzdb-project/fuzzdb
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `discovery-predictable-filepaths/` | 路径字典 |
| `attack-payloads/` | 按漏洞类型的 payload 集 |
| `regex/` | 错误指纹正则 |
| `wordlists-user-passwd/` | 弱口令字典 |

## 攻击场景 Playbook

### 手工构造模糊测试

```bash
ffuf -u https://t.com/FUZZ -w fuzzdb/discovery-payloads/.../common.txt
sqlmap -r req.txt --prefix-file=fuzzdb/attack-payloads/sql-injection/detect/...
```

## 注意事项

经典 fuzz 字典库,与 SecLists 互补;无代码全是语料,Agent 直接引用路径即可。
