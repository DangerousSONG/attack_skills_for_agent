---
name: arjun-param-discovery
description: Arjun: 隐藏参数挖掘→扩大攻击面。信号:web扫描,漏洞扫描,HTTP 参数发现,POST 方法,降低速率防 WAF。
---

# Arjun

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/s0md3v/Arjun
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install arjun
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `arjun -u https://api.target.com/endpoint` | HTTP 参数发现 |
| `-m POST` | POST 方法 |
| `--stable` | 降低速率防 WAF |
| `-t 20` | 线程 |
| `-oJ out.json` | JSON 输出 |

## 攻击场景 Playbook

### 隐藏参数挖掘→扩大攻击面

```bash
arjun -u https://api.target.com/v1/users -m GET,POST -oJ params.json
# 发现的 admin/debug/id 等参数转交 ffuf 深度测
```

## 注意事项

基于响应差异(长度/状态码)探测未文档参数;JS 里常先扒一遍参数名再跑。
