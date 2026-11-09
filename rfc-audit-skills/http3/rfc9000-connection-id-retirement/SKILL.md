---
name: rfc9000-connection-id-retirement
description: 审计 QUIC 实现对 Connection ID 生命周期（NEW_CONNECTION_ID / RETIRE_CONNECTION_ID / active_connection_id_limit）义务的处理是否对称——义务不对称即存在内存耗尽攻击面（关联 CVE-2024-22189，7.5 HIGH）
rfc: RFC 9000 §5.1（Connection IDs）/ §19（Frame 处理规则）
license: Apache-2.0
---

# RFC 9000 §5.1 Connection ID 生命周期义务对称性审计

## 1. 约束条款（原文出处）

RFC 9000 §5.1.2：端点发送 NEW_CONNECTION_ID 后，对端可用 RETIRE_CONNECTION_ID 要求退役；**收到 RETIRE_CONNECTION_ID 的端点必须停止使用该 CID 并以 RETIRE_CONNECTION_ID 确认（帧义务成对出现）**。

RFC 9000 §5.1.1：`active_connection_id_limit` 传输参数限制对端可处于激活状态的 CID 数量；达到上限前**不得**发出新的 NEW_CONNECTION_ID。

§19.16：RETIRE_CONNECTION_ID 帧对当前仍在使用的 CID、或从未由对端分配的 CID 的引用，必须按协议错误（FRAME_ENCODING_ERROR）处理。

核心模式一句话：**协议为状态对象定义了"分配-使用-退役"的成对义务，义务不对称（一方必须维护状态、另一方可以低成本触发）即被武器化。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| CI-1 | 快速连续发送大量 NEW_CONNECTION_ID 并立即 RETIRE，迫使对端为每次退役维护响应状态 | 对端内存随迭代次数单调增长且无上限 → 漏洞 |
| CI-2 | 通过选择性 ACK + RTT 操纵压制对端拥塞窗口，使其 RETIRE_CONNECTION_ID 响应排队（CVE-2024-22189 精确时序） | 响应义务被积压、状态无界增长 → 漏洞 |
| CI-3 | 发送 NEW_CONNECTION_ID 使对端激活 CID 数超过其声明的 `active_connection_id_limit` | 未按协议错误处理/未强制上限 → 违规 |
| CI-4 | RETIRE 引用当前 active CID 或对端从未分配的 CID | 未返回 FRAME_ENCODING_ERROR → 帧校验不严 |

判定方法：aioquic 帧级脚本；观测对端内存曲线与连接错误码。

## 3. 攻击面猜想

未认证远程内存耗尽：攻击成本 = 小流量帧序列，目标成本 = 每轮迭代一份不可释放的 CID 状态（CVE-2024-22189 实测可耗尽）。CI-3/CI-4 的校验不严是独立攻击面（状态机混淆），也常与 CI-1 组合。

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2024-22189**（7.5 HIGH） | QUIC 多家实现（以 quic-go 为代表披露） | 攻击者洪泛 NEW_CONNECTION_ID 并退役旧 CID，接收方须为每次退役回 RETIRE_CONNECTION_ID；攻击者靠选择性 ACK 压垮对端拥塞窗口+操纵 RTT，使响应无法发出，状态无限堆积直至内存耗尽 |

## 5. 差分验证方法

对照组：quic-go 修复版（≥0.43）、ngtcp2。
对比字段：CI-1 迭代 1k/10k/100k 轮的内存曲线斜率；CI-2 时序压制下响应延迟；CI-3/CI-4 的错误码。
误报排除：实现可选地主动限制 CID 发放速率属合规加固；只标记"义务不对称可被强制"的实现。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（状态机差分）、`slowhttptest-dos`（资源耗尽验证；均在 tool-skills/）
- 工具层（用什么打）：aioquic（帧级时序控制主力）、quic-go 客户端做对照
- 命中后动作：量化每轮迭代的状态堆积量 → 给出 N 轮内存耗尽的时间估计 → 输出影响版本面
