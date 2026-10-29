---
name: wafninja-waf-bypass
description: "WAFNinja: WAF fingerprinting plus bypass retries. Signals: web vulnerabilities, injection, SQLi payload, identify WAF vendor, custom payload."
zh-signals: "WAFNinja: WAF 指纹+绕过重试。信号:web漏洞,注入,SQLi payload,识别 WAF 厂商,自定义 payload。"
---

# WAFNinja

- 攻击大类:C09 Web利用(WAF绕过)
- 上游仓库:https://github.com/khalilbijjou/WAFNinja
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/khalilbijjou/WAFNinja && cd WAFNinja && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wafninja.py -u 'https://t.com/?id=1' -t xss` | XSS payload 批量测 |
| `-t sqli` | SQLi payload |
| `--fingerprint` | 识别 WAF 厂商 |
| `-p 'payload'` | 自定义 payload |

## 攻击场景 Playbook

### WAF 指纹+绕过重试

```bash
python wafninja.py -u 'https://t.com/?q=x' --fingerprint
python wafninja.py -u 'https://t.com/?q=x' -t sqli
# 观察哪条 payload 不再被 403
```

## 注意事项

payload 库+WAF 指纹识别,被拦时快速定位 WAF 类型并尝试变形绕过。
