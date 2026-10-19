---
name: hakrawler-fast-crawler
description: 渗透工具 skill:hakrawler 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 hakrawler 时使用。
---

# hakrawler

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/hakluke/hakrawler
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/hakluke/hakrawler@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `echo https://target.com | hakrawler` | 爬取端点/表单/JS |
| `-d 3` | 爬深 3 层 |
| `-subs` | 包含子域 |
| `-u` | 显示来源 URL |
| `-t 20` | 线程 |
| `-insecure` | 忽略 TLS 错误 |
| `-proxy http://127.0.0.1:8080` | 过代理 |

## 攻击场景 Playbook

### 站点端点快速收割

```bash
echo https://app.target.com | hakrawler -d 2 -subs | sort -u > endpoints.txt
grep -E '\?.*=' endpoints.txt > params.txt  # 送参数字典爆破
```

## 注意事项

Go 写的快爬虫,输出纯文本适合管道;表单和 JS 发现能力适合喂给 fuzzer。
