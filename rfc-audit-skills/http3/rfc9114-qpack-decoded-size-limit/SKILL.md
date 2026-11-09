---
name: rfc9114-qpack-decoded-size-limit
description: 审计 HTTP/3 目标是否只对 QPACK 压缩后帧长限长、而未对解压后字段区块限长——未限长即存在压缩放大内存耗尽攻击面（单连接可达数千倍放大；关联 CVE-2025-64702/CVE-2026-40898 quic-go、CVE-2026-12523 quiche、CVE-2025-13945 Wireshark）
rfc: RFC 9114 §4.1.1 + RFC 9204（QPACK）
license: Apache-2.0
---

# RFC 9114 §4.1.1 / RFC 9204 解码后字段区块限长审计（QPACK 压缩放大）

## 1. 约束条款（原文出处）

RFC 9114 §4.1.1：HTTP/3 实现对字段区块大小施加上限（field section size limit），超限必须以 `H3_EXCESSIVE_LOAD` 中止。

RFC 9204（QPACK）：动态表使小压缩载荷可解码出大量大字段——**限长必须作用于解码后的字段区块，而非线上压缩帧**。

根因模式一句话：**对线上帧长限长 ≠ 对解码后内容限长**；压缩比可达数百至数千倍，单连接即可耗尽内存。

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| QS-1 | 发送压缩后 ≈1KB、解码后 ≈1~10MB 的 HEADERS 帧（大量唯一字段名/大值，经 QPACK 动态表压缩） | 目标进程内存显著上涨且未中止流 → 违规；流被 H3_EXCESSIVE_LOAD 重置 → 合规 |
| QS-2 | 同 QS-1，但把大字段放入 **trailer 区块**（HEADERS 帧跟在 DATA 之后） | trailer 是常见漏检点（CVE-2026-40898 攻击向量），单独判定 |
| QS-3 | 观察目标限长粒度：逐条解码边解边查，还是整体解完再查 | 整体解完再查在大载荷下同样可被耗尽（修复版 quic-go 0.59.1 的做法是逐条解码+逐条检查） |

判定方法：h3i / aioquic 构造 QPACK 动态表压缩帧；观测目标 RSS / OOM 行为。

## 3. 攻击面猜想

未认证远程 DoS：单连接以小流量迫使服务端分配大内存（CWE-770），可打挂 Caddy / Traefik / cloudflared 等依赖库的任何下游产品。对称存在于客户端（恶意服务端打客户端）。

## 4. 关联历史 CVE（同类模式跨实现复现——本 Skill 的核心价值）

| CVE | 实现 | 说明 |
|---|---|---|
| **CVE-2025-64702** | quic-go ≤0.56.0 | 头部区块：只对压缩帧限长（`maxHeaderBytes` 比较的是 `hf.Length`），解码后无限长。修复于 0.57.0 |
| **CVE-2026-40898** | quic-go <0.59.1 | trailer 区块同类。修复：对 trailer 也强制执行 RFC 9114 解码后字段区块限长，逐条解码逐条检查 |
| **CVE-2026-12523** | Cloudflare quiche <0.29.3 | FoxIO 批量发现的同模式（2026-10 公开 PoC） |
| **CVE-2025-13945** | Wireshark <4.6.2/4.4.12 | 同模式（解析器侧） |
| 未修复 | Bun、h3(Rust)、aioquic | FoxIO 报告时仍未修补，Bun 有计数器溢出导致 CPU 100% 的变体 |

## 5. 差分验证方法

对照组：quic-go 0.59.1（合规基线）、quiche 0.29.3。
对比字段：QS-1/QS-2 探测下目标内存增量、是否中止流及错误码、放大倍数。
误报排除：目标声明了超大 field section limit 且按文档工作——属配置问题非实现漏洞，单独标记。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（协议 fuzz 框架）、`slowhttptest-dos`（DoS 验证思路；均在 tool-skills/）
- 工具层（用什么打）：h3i、foxio QPACK PoC（2026-10 已公开）、aioquic
- 命中后动作：按依赖链上报（库 → 下游产品 Caddy/Traefik/cloudflared/LiteSpeed），输出放大倍数与影响面评估
