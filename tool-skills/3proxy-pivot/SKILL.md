---
name: 3proxy-pivot
description: 3proxy: 已控主机上起二级代理供全组使用。信号:内网穿透,隧道,SOCKS5,仅按 IP 白名单放行。
---

# 3proxy

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/3proxy/3proxy
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/3proxy/3proxy && make -f Makefile.Linux
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `proxy -p3128 -i0.0.0.0 -e0.0.0.0` | 起 HTTP/SOCKS 代理 |
| `socks -p1080` | SOCKS5 |
| `auth iponly / allow * * * *` | 仅按 IP 白名单放行 |

## 攻击场景 Playbook

### 已控主机上起二级代理供全组使用

```bash
./3proxy proxy -p3128 -i0.0.0.0 -e0.0.0.0 &
# 攻击机: proxychains curl http://内网IP/
```

## 注意事项

极小体积 C 语言代理,Windows/Linux 通吃;配合 ssh -R 反向暴露到攻击机。
