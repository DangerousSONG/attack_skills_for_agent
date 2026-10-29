---
name: crlfuzz-crlf-injection
description: "CRLFuzz: Tests response splitting via CRLF injection. Signals: web vulnerability, injection, single-target CRLF injection, batch."
zh-signals: "CRLFuzz: 响应拆分测试。信号:web漏洞,注入,单目标 CRLF 注入,批量。"
---

# CRLFuzz

- 攻击大类:C09 Web利用(CRLF/HTTP头注入)
- 上游仓库:https://github.com/dwisiswant0/crlfuzz
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/dwisiswant0/crlfuzz/cmd/crlfuzz@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `crlfuzz -u 'https://t.com/?url=x'` | 单目标 CRLF 注入 |
| `-l urls.txt` | 批量 |
| `-o out.txt` | 输出 |
| `-s` | 静默模式 |

## 攻击场景 Playbook

### 响应拆分测试

```bash
crlfuzz -u 'https://t.com/redirect?next=https://a.com'
# 命中后注入 Set-Cookie / 302 Location 头
```

## 注意事项

Go 编写,快,对 URL 每个参数注入 CRLF(%0d%0a)并检测响应头回显。
