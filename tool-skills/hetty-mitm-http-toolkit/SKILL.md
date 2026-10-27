---
name: hetty-mitm-http-toolkit
description: hetty: HTTPS 流量拦截改包测试。信号:中间人,mitm,链上游代理,限定拦截域名避免噪音。
---

# hetty

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/dstotijn/hetty
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/dstotijn/hetty/cmd/hetty@latest 或下 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `hetty --cert-store ./certs` | 启动 MITM 代理(:8080 + 管理界面:31337) |
| `--proxy http://upstream:3128` | 链上游代理 |
| `scope 配置` | 限定拦截域名避免噪音 |

## 攻击场景 Playbook

### HTTPS 流量拦截改包测试

```bash
hetty --cert-store ./certs
# 浏览器/手机装 hetty CA 证书后代理到 :8080,在 Web 界面拦截重放改包
```

## 注意事项

Go 版 Burp 替代品,资源占用低,适合长期挂代理;证书存 ./certs 可复用。
