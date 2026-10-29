---
name: yasuo-vuln-scan
description: "yasuo: Admin panel and vulnerability dual detection. Signals: web vulnerability, injection, web app vulnerability scan, all ports, brute-force admin panel."
zh-signals: "yasuo: 后台+漏洞双探测。信号:web漏洞,注入,Web 应用漏洞扫描,全端口,爆破后台。"
---

# yasuo

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/0xsauby/yasuo
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xsauby/yasuo && cd yasuo
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ruby yasuo.rb -r hosts.txt -p 80,8080` | Web 应用漏洞扫描 |
| `-r file -f` | 全端口 |
| `-b` | 爆破后台 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 后台+漏洞双探测

```bash
ruby yasuo.rb -r ips.txt -p 80,443,8080
# 识别应用类型+默认后台+已知漏洞
```

## 注意事项

Web 应用指纹识别+漏洞扫描,适合大 IP 段批量。
