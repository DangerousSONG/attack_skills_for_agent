---
name: goofuzz-google-dork
description: 渗透工具 skill:GooFuzz 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 GooFuzz 时使用。
when-to-use: 渗透工具 skill:GooFuzz 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 GooFuzz 时使用。
---

# GooFuzz

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/m3n0sd0n4ld/GooFuzz
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/m3n0sd0n4ld/GooFuzz && cd GooFuzz
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./GooFuzz -t corp.com` | Google dork 批量探测 |
| `-t target -d '/admin|/backup'` | 自定义 dork |
| `-e pdf,xls` | 文件类型 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 免 API key 的 Google dork

```bash
./GooFuzz -t corp.com -w wordlists/ghdb.txt
# 自动翻页采结果,撞库目标敏感文件索引
```

## 注意事项

纯 bash Google dork 工具,无需 API key,内置 GHDB 分类词库。
