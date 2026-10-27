---
name: altdns-permutation
description: altdns: 已知子域变形爆破。信号:子域名,域名枚举,置换生成候选子域,生成后解析,线程。
---

# altdns

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/infosec-au/altdns
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install py-altdns
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `altdns -i known.txt -o permutations.txt -w words.txt` | 置换生成候选子域 |
| `-r -s resolved.txt` | 生成后解析 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### 已知子域变形爆破

```bash
altdns -i subs.txt -o cand.txt -w ~/tools/words.txt -r -s resolved.txt
# 基于已知子域模式生成 dev-api/api-dev 等置换并解析
```

## 注意事项

解决'已知子域之外的未知模式';配 massdns/puredns 解析效果最佳。
