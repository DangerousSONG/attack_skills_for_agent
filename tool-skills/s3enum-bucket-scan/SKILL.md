---
name: s3enum-bucket-scan
description: s3enum: S3 桶发现(错配公开)。信号:攻击面,云资产,S3 bucket 枚举,常用后缀,并发。
---

# s3enum

- 攻击大类:C05 云资产发现
- 上游仓库:https://github.com/koenrh/s3enum
- 上游 License:ISC(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/koenrh/s3enum@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `s3enum -wordlist ~/wordlists/buckets.txt -suffixes '' corp` | S3 bucket 枚举 |
| `-suffixes '-dev,-backup,-logs'` | 常用后缀 |
| `-threads 10` | 并发 |

## 攻击场景 Playbook

### S3 桶发现(错配公开)

```bash
s3enum -wordlist buckets.txt corp
# 命中后 aws s3 ls s3://bucket 看是否有公开数据
```

## 注意事项

DNS 排列组合枚举 S3 桶名,找到疑似目标后手动验证公开访问/写权限。
