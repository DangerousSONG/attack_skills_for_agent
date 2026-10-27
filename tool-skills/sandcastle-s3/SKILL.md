---
name: sandcastle-s3
description: sandcastle: S3 桶名爆破。信号:攻击面,云资产,S3 bucket 发现,字典。
---

# sandcastle

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/0xSearches/sandcastle
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xSearches/sandcastle
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 sandcastle.py -t corp` | S3 bucket 发现 |
| `-t target -b buckets.txt` | 字典 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### S3 桶名爆破

```bash
python3 sandcastle.py -t corp
# 常见命名规律遍历
```

## 注意事项

S3 bucket 轻量枚举。
