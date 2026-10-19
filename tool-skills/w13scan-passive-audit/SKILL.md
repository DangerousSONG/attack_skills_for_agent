---
name: w13scan-passive-audit
description: 渗透工具 skill:w13scan 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 w13scan 时使用。
---

# w13scan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/boy-hack/w13scan
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/boy-hack/w13scan && cd w13scan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 w13scan.py -u https://t.com` | 被动扫描 |
| `-u url --proxy` | 代理模式抓流量 |
| `-p 8080` | 代理端口 |
| `--level 5` | 检测等级 |

## 攻击场景 Playbook

### 被动流量漏洞审计

```bash
python3 w13scan.py -u https://t.com -p 8080
# 浏览器过代理浏览全站,被动分析每个请求
```

## 注意事项

被动式 Web 漏洞扫描器,基于流量分析,适合授权测试中的全站审计。
