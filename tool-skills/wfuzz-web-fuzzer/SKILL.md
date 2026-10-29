---
name: wfuzz-web-fuzzer
description: "wfuzz: Full-position fuzzing. Signals: web scanning, vulnerability scanning, directory brute force, POST fuzz, header fuzz."
zh-signals: "wfuzz: 全位置模糊测试。信号:web扫描,漏洞扫描,目录爆破,POST fuzz,Header fuzz。"
---

# wfuzz

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/xmendez/wfuzz
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install wfuzz
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-w /usr/share/wfuzz/wordlist/general/common.txt https://t.com/FUZZ` | 目录爆破 |
| `-w words.txt -d 'id=FUZZ&name=x'` | POST fuzz |
| `-w payloads.txt -H 'X-Header: FUZZ'` | Header fuzz |
| `--hc=404` | 隐藏 404 |
| `--hh=889` | 按长度过滤 |
| `-t 50` | 线程 |
| `-o csv` | 输出 |
| `-z list,admin-root-test` | 值列表 |

## 攻击场景 Playbook

### 全位置模糊测试

```bash
wfuzz -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt --hc 404 https://target/FUZZ
wfuzz -w sql-errors.txt -d 'id=FUZZ' --hh=1200 https://target/search.php  # SQLi 错误指纹探测
```

## 注意事项

HTTP fuzz 老牌标杆;FUZZ 占位符可在 URL/POST/Header/Cookie 任意位置。
