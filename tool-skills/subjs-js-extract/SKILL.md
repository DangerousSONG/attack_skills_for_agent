---
name: subjs-js-extract
description: subjs: JS 文件批量提取。信号:web漏洞,注入,subjs`,并发。
---

# subjs

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/lc/subjs
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/lc/subjs@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat urls.txt | subjs` | 从 URL 提取 JS 链接 |
| `-c 20` | 并发 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### JS 文件批量提取

```bash
cat gau_urls.txt | subjs | tee js.txt
# 喂给 nuclei/secret 扫描
```

## 注意事项

从 HTML 页面批量提取 <script src>,常与 gau 组合使用。
