---
name: gau-url-history
description: 渗透工具 skill:gau (Get All URLs) 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 gau (Get All URLs) 时使用。
when-to-use: 渗透工具 skill:gau (Get All URLs) 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 gau (Get All URLs) 时使用。
---

# gau (Get All URLs)

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/lc/gau
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gau example.com` | OTX+Wayback+CommonCrawl+URLScan 全源拉取 |
| `--subs` | 包含子域名 |
| `--threads 5` | 并发数 |
| `--blacklist png,jpg` | 过滤静态资源 |
| `--fc 404` | 过滤状态码(需 --json 先存) |

## 攻击场景 Playbook

### 历史端点收集→喂给漏洞扫描

```bash
gau --subs target.com | grep -E '\.(php|asp|aspx|jsp)' | sort -u > endpoints.txt
nuclei -l endpoints.txt -t exposures/
```

### JS 文件敏感信息挖掘

```bash
gau target.com | grep '\.js$' | httpx -silent | tee js.txt
while read u; do curl -s $u | grep -Eo '(api[_-]?key|token|secret)[^,]{0,80}'; done < js.txt
```

## 注意事项

被动历史数据源,不触目标,适合授权边界内先做情报面收敛。
