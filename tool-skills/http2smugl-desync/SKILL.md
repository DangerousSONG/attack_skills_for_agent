---
name: http2smugl-desync
description: "http2smugl detects HTTP/2 request smuggling. Signals: web vulnerability, injection, second obfuscation mode, inject smuggling prefix, report only exploitable targets."
zh-signals: "http2smugl: HTTP/2 走私检测。信号:web漏洞,注入,第二种混淆模式,注入走私前缀,只报可利用目标。"
---

# http2smugl

- 攻击大类:C09 Web利用(HTTP走私)
- 上游仓库:https://github.com/neex/http2smugl
- 上游 License:Unlicense(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/neex/http2smugl && cd http2smugl && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `http2smugl -u 'https://t.com/' -t CL.TE` | HTTP/2→1.1 请求走私检测 |
| `-t TE.CL` | 第二种混淆模式 |
| `-c 'x=1'` | 注入走私前缀 |
| `--vulnerable-only` | 只报可利用目标 |

## 攻击场景 Playbook

### HTTP/2 走私检测

```bash
http2smugl -u 'https://t.com/' -t CL.TE
# 命中后构造 CL.TE 前缀走私任意请求到后端
```

## 注意事项

专攻 HTTP/2 到 HTTP/1.1 转换时的走私面(CL.TE/TE.CL 混淆)。
