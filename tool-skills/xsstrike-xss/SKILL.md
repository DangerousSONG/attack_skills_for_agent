---
name: xsstrike-xss
description: "XSStrike: Intelligent XSS detection. Signals: web vulnerability, injection, automatic XSS detection, site crawl scan, POST."
zh-signals: "XSStrike: 智能 XSS 打点。信号:web漏洞,注入,自动 XSS 检测,爬站扫,POST。"
---

# XSStrike

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/s0md3v/XSStrike
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/s0md3v/XSStrike && cd XSStrike && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python xsstrike.py -u 'https://t.com/search?q=test'` | 自动 XSS 检测 |
| `--crawl` | 爬站扫 |
| `--data 'q=1'` | POST |
| `--headers` | 注入 header |
| `-t 5` | 线程 |
| `--file-log` | 保存结果 |
| `--path` | path 型 XSS |
| `--fuzzer` | fuzz 模式 |

## 攻击场景 Playbook

### 智能 XSS 打点

```bash
python xsstrike.py -u 'https://target/search?q=hello' --crawl
# 内置 7 个解析器,生成上下文感知 payload,成功率高于通用扫描器
```

## 注意事项

payload 按反射上下文动态生成(不是字典跑);爬站模式适合批量资产初筛。
