---
name: zdns-lookup
description: ZDNS: 百万级 DNS 查询。信号:资产测绘,指纹识别,zdns A`,MX 记录,NS 记录。
---

# ZDNS

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/zmap/zdns
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/zmap/zdns@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `echo corp.com | zdns A` | 批量 A 记录解析 |
| `zdns MX --name-servers 8.8.8.8` | MX 记录 |
| `zdns NS` | NS 记录 |
| `zdns A --output-file out.json` | JSON 输出 |

## 攻击场景 Playbook

### 百万级 DNS 查询

```bash
cat subs.txt | zdns A --threads 1000 -o resolved.jsonl
jq -r '.data.answers[]? | select(.type=="A") | .answer' resolved.jsonl
```

## 注意事项

ZMap 团队的 DNS 引擎;百万级查询分钟级完成,比 dnsx 更极限。
