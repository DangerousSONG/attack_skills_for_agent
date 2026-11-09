---
name: torpy-tor-client
description: "torpy makes anonymous requests over Tor. Signals: internal pivoting, tunneling, Tor client, execute over Tor, hops"
zh-signals: "torpy: Tor 网络匿名请求。信号:内网穿透,隧道,Tor 客户端,Tor 内执行,跳数。"
---

# torpy

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/torpyorg/torpy
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install torpy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python -m torpy -h` | Tor 客户端 |
| `-c 'curl http://target'` | Tor 内执行 |
| `--hops 3` | 跳数 |

## 攻击场景 Playbook

### Tor 网络匿名请求

```bash
python -m torpy -c 'curl https://ifconfig.me'
# 无需 Tor Browser,脚本化
```

## 注意事项

纯 Python Tor 客户端,脚本化 Tor 网络访问。
