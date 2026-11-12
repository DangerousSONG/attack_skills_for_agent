---
name: torpy-tor-client
description: "torpy makes anonymous requests over Tor. Signals: internal pivoting, tunneling, Tor client, execute over Tor, hops"
zh-signals: "torpy: Tor 网络匿名请求。信号:内网穿透,隧道,Tor 客户端,Tor 内执行,跳数。"
when-to-use: "Use torpy when you need scriptable, anonymous requests over the Tor network, such as routing curl commands through Tor with a configurable number of hops for pivoting or anonymity."
---

# torpy

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/torpyorg/torpy
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install torpy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python -m torpy -h` | Tor client |
| `-c 'curl http://target'` | Execute over Tor |
| `--hops 3` | Number of hops |

## Attack Scenario Playbook

### Anonymous requests over the Tor network

```bash
python -m torpy -c 'curl https://ifconfig.me'
# No Tor Browser needed, fully scriptable
```

## Notes

A pure-Python Tor client for scriptable access to the Tor network.
