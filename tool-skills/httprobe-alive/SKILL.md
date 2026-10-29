---
name: httprobe-alive
description: "httprobe filters subdomains to live sites. Signals: port scan, nmap, httprobe, concurrency, timeout ms."
zh-signals: "httprobe: 子域→存活站点过滤。信号:端口扫描,nmap,httprobe`,并发,超时 ms。"
---

# httprobe

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/tomnomnom/httprobe
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/tomnomnom/httprobe@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat hosts.txt | httprobe` | 批量探 HTTP/HTTPS 存活 |
| `-c 50` | 并发 |
| `-t 10000` | 超时 ms |
| `-p xlarge` | 大端口集 |
| `-s` | 只 HTTPS |

## 攻击场景 Playbook

### 子域→存活站点过滤

```bash
subfinder -d corp.com -silent | httprobe -c 100 | tee alive.txt
cat alive.txt | aquatone  # 下游截图/指纹
```

## 注意事项

pd 流水线标配件;stdin 进 stdout 出,与其他工具零摩擦对接。
