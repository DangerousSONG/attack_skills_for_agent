---
name: dcrawl-fast-crawl
description: dcrawl: 批量 URL 轻爬。信号:资产测绘,指纹识别,批量快速爬取,深度。
---

# dcrawl

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/kgretzky/dcrawl
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/kgretzky/dcrawl@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dcrawl -list urls.txt` | 批量快速爬取 |
| `-depth 2` | 深度 |
| `-out out.txt` | 输出 |
| `-timeout 5` | 超时 |

## 攻击场景 Playbook

### 批量 URL 轻爬

```bash
dcrawl -list alive.txt -depth 2
# 只提链接不去内容,超快
```

## 注意事项

kgretzky 出品,纯链接提取爬虫,速度优于 htcap。
