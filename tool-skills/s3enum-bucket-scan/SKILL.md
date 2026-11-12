---
name: s3enum-bucket-scan
description: "s3enum: Discovers misconfigured public S3 buckets. Signals: attack surface, cloud assets, S3 bucket enumeration, common suffixes, concurrency."
zh-signals: "s3enum: S3 桶发现(错配公开)。信号:攻击面,云资产,S3 bucket 枚举,常用后缀,并发。"
when-to-use: >-
  Use when hunting for misconfigured public S3 buckets by enumerating bucket names
  from wordlists and common suffixes for a target organization.
---

# s3enum

- Attack Category: C05 Cloud Asset Discovery
- Upstream Repository: https://github.com/koenrh/s3enum
- Upstream License: ISC (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/koenrh/s3enum@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `s3enum -wordlist ~/wordlists/buckets.txt -suffixes '' corp` | S3 bucket enumeration |
| `-suffixes '-dev,-backup,-logs'` | Common suffixes |
| `-threads 10` | Concurrency |

## Attack Scenario Playbook

### S3 Bucket Discovery (Misconfigured Public Access)

```bash
s3enum -wordlist buckets.txt corp
# On a hit, run aws s3 ls s3://bucket to check for public data
```

## Notes

Enumerates S3 bucket names through DNS permutations, then manually verify public access or write permissions on suspected targets.
