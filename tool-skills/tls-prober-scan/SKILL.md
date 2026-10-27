---
name: tls-prober-scan
description: tls-prober: TLS 栈指纹识别。信号:资产测绘,指纹识别,TLS 实现指纹,CSV 输出。
---

# tls-prober

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/x42/tls-prober
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/x42/tls-prober
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python prober.py -p 443,8443 targets.txt` | TLS 实现指纹 |
| `-o out.csv` | CSV 输出 |

## 攻击场景 Playbook

### TLS 栈指纹识别

```bash
python prober.py targets.txt  # 识别 OpenSSL/GnuTLS/IIS 版本,缩小 CVE 范围
```

## 注意事项

TLS ClientHello 探测指纹 TLS 库;常与 nmap 服务识别互补。
