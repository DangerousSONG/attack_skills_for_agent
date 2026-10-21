---
name: gospider-js-crawl
description: 渗透工具 skill:gospider 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 gospider 时使用。
when-to-use: 渗透工具 skill:gospider 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 gospider 时使用。
---

# gospider

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/jaeles-project/gospider
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/jaeles-project/gospider@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gospider -s https://t.com` | 整站爬取(URL/JS/表单) |
| `-S urls.txt` | 批量 |
| `-d 3` | 深度 |
| `--js` | 解析 JS 提取端点 |
| `-o out/` | 输出 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### JS 端点提取喂漏扫

```bash
gospider -S live_hosts.txt -d 3 --js -o spider/
# 从 JS bundle 提 API 端点/参数,交 dalfox/nuclei
```

## 注意事项

jaeles 生态的爬虫,JS 渲染+源映射解析,输出可直接接 nuclei/dalfox 的 URL 清单。
