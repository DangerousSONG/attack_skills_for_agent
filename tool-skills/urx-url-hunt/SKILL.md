---
name: urx-url-hunt
description: "urx: Multi-source URL aggregation. Signals: data collection, packing, pipeline filtering, concurrency."
zh-signals: "urx: 多源 URL 聚合。信号:数据收集,打包,管道过滤,并发。"
---

# urx

- 攻击大类:C33 URL与内容发现
- 上游仓库:https://github.com/hahwul/urx
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install urx
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `urx -u https://t.com` | 多源 URL 收割(Wayback/CC/OTX) |
| `--pipe 'grep admin'` | 管道过滤 |
| `-o out.txt` | 输出 |
| `-c 50` | 并发 |
| `--include-wayback --include-otx` | 指定数据源 |

## 攻击场景 Playbook

### 多源 URL 聚合

```bash
urx -u https://t.com --pipe 'grep -Ei "api|admin|token"' | tee gold.txt
# 各源结果去重合并且同时输出原始和去重 URL
```

## 注意事项

Rust 编写的高速 URL 聚合器,一次查询 Wayback Machine/Common Crawl/AlienVault OTX 等多源。
