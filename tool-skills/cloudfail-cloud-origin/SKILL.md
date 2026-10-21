---
name: cloudfail-cloud-origin
description: 渗透工具 skill:CloudFail 的安装、参数速查与攻击场景 playbook。当任务涉及 痕迹清理与反取证 需要调用 CloudFail 时使用。
when-to-use: 渗透工具 skill:CloudFail 的安装、参数速查与攻击场景 playbook。当任务涉及 痕迹清理与反取证 需要调用 CloudFail 时使用。
---

# CloudFail

- 攻击大类:C50 痕迹清理与反取证
- 上游仓库:https://github.com/m0rtem/CloudFail
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/m0rtem/CloudFail && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 cloudfail.py --target t.com` | 绕过 CF 找源站 IP |
| `-s` | 扫描全部子域 |
| `--tor` | Tor 出口防封 |

## 攻击场景 Playbook

### CDN 后源站 IP 定位

```bash
python3 cloudfail.py --target t.com --tor
# 历史 DNS 记录+子域旁路,拿到源站直接绕 WAF
```

## 注意事项

利用历史 DNS 数据和非 CDN 子域定位 Cloudflare 后的真实源站。
