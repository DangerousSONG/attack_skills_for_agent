---
name: fuzzowski-network-fuzz
description: "fuzzowski provides introductory private protocol fuzzing. Signals: pwn, binary exploitation, FTP protocol fuzzing, HTTP fuzzing, custom request scripts."
zh-signals: "fuzzowski: 私有协议 fuzz 入门。信号:pwn,二进制利用,FTP 协议 fuzz,HTTP fuzz,自定义请求脚本。"
---

# fuzzowski

- 攻击大类:C46 模糊测试与漏洞挖掘
- 上游仓库:https://github.com/nccgroup/fuzzowski
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install fuzzowski
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `fuzzowski -f ftp -t 10.0.0.1` | FTP 协议 fuzz |
| `-f http -t url` | HTTP fuzz |
| `-f fuzzowski/requests/http_request.py -t target` | 自定义请求脚本 |
| `-n 10` | 迭代次数 |

## 攻击场景 Playbook

### 私有协议 fuzz 入门

```bash
fuzzowski -f ftp -t 10.0.0.1 -x
# Sulley 继任者,响应监控+崩溃自动记录,二进制协议测试
```

## 注意事项

NCC 出品,Sulley 精神续作,网络协议 fuzz 框架,内置 FTP/HTTP 等协议模板。
