---
name: zgrab2-banner
description: zgrab2: 全网资产应用层指纹。信号:资产测绘,指纹识别,TLS 证书/指纹,SSH banner,JSON 输出。
---

# zgrab2

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/zmap/zgrab2
- 上游 License:NOASSERTION(Apache-2.0 为主)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/zmap/zgrab2@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `zgrab2 http -p 80,8080 < ips.txt` | HTTP banner 抓取 |
| `zgrab2 tls -p 443` | TLS 证书/指纹 |
| `zgrab2 ssh` | SSH banner |
| `-o out.json` | JSON 输出 |

## 攻击场景 Playbook

### 全网资产应用层指纹

```bash
zmap -p 443 -o ips.txt 10.0.0.0/8
zgrab2 http tls -p 443,8443 -o banners.json < ips.txt
jq -r '.tls.server_certificates[0].parsed.subject.common_name[]?' banners.json | sort -u  # 证书域名提取
```

## 注意事项

ZMap 官方应用层搭档;从 IP 列表批量抓 banner/证书/JA3。
