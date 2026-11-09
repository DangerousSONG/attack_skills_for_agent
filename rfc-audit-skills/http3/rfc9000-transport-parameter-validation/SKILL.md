---
name: rfc9000-transport-parameter-validation
description: 审计 QUIC 实现对传输参数完整性与一致性校验是否按 RFC 9000 §18.2/§7.3——CID 相关参数缺失/错配、服务端专用参数被客户端携带、非法值未拒绝即握手前无认证攻击面与中间人注入 CID 面
rfc: RFC 9000 §18.2（Transport Parameter 定义）/ §7.3（使用 CID 参数的验证义务）
license: Apache-2.0
---

# RFC 9000 §18.2 传输参数校验完备性审计

## 1. 约束条款（原文出处）

RFC 9000 §7.3/§18.2（原文要点）：
> An endpoint MUST treat the absence of the initial_source_connection_id transport parameter from either endpoint or the absence of the original_destination_connection_id transport parameter from the server as a connection error of type TRANSPORT_PARAMETER_ERROR.
> An endpoint MUST treat the following as a connection error of type TRANSPORT_PARAMETER_ERROR or PROTOCOL_VIOLATION: absence of the retry_source_connection_id transport parameter from the server after receiving a Retry packet; presence of the retry_source_connection_id transport parameter when no Retry packet was received; or a mismatch between values received from a peer in these transport parameters and the value sent in the corresponding Destination or Source Connection ID fields of Initial packets.
> A client MUST NOT include any server-only transport parameter: original_destination_connection_id, preferred_address, retry_source_connection_id, or stateless_reset_token. A server MUST treat receipt of any of these transport parameters as a connection error of type TRANSPORT_PARAMETER_ERROR.
> A server that chooses a zero-length connection ID MUST NOT provide a preferred address. Similarly, a server MUST NOT include a zero-length connection ID in this transport parameter. A client MUST treat a violation of these requirements as a connection error of type TRANSPORT_PARAMETER_ERROR.
> max_udp_payload_size 值低于 1200 为无效。

核心模式一句话：**CID 相关传输参数是把"线路上看到的 CID"与"握手协商出的 CID"绑定的唯一锚——锚缺失或错配意味着握手期间的 Initial 可被注入替换，整个连接的身份从握手第一包起就可能是攻击者选定的。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| TP-1 | 删除 initial_source_connection_id（或服务端删除 original_destination_connection_id）后完成握手 | 未以 TRANSPORT_PARAMETER_ERROR 终止 → 违规 |
| TP-2 | 无 Retry 路径下携带 retry_source_connection_id / 有 Retry 路径下缺失该参数 / 参数值与 Retry 包 SCID 不符 | 未终止 → 违规 |
| TP-3 | 客户端 Initial 携带服务端专用参数（original_destination_connection_id / preferred_address / retry_source_connection_id / stateless_reset_token 任一） | 服务端未终止 → 违规 |
| TP-4 | 构造传输参数值与线路 Initial 包 CID 字段不一致（改写 DCID 重放） | 未检测 → 中间人可注入自选 CID 成立 |
| TP-5 | 发送 max_udp_payload_size < 1200 / preferred_address 含零长 CID / 零长 CID 服务端带 preferred_address | 未按 TRANSPORT_PARAMETER_ERROR 终止 → 违规 |

判定方法：aioquic 逐参数篡改（传输参数位于加密扩展，需自写 TLS 层或借助支持扩展的栈）；quic-go 调试日志观测校验路径。

## 3. 攻击面猜想

- **CID 注入（中间人）**：TP-4 ——握手期注入带攻击者选定 CID 的 Initial，若校验缺失则连接身份被劫持，后续路由/无状态重置令牌全部错位
- **无认证握手前崩溃**：传输参数解析处于握手前路径，畸形参数是 LSQUIC QUIC-LEAK（CVE-2025-54939）同类"smuggled 包触发内存分配"的入口
- **preferred_address 零长 CID**：可导致迁移路径上的连接 ID 状态机进入未定义分支

## 4. 关联历史 CVE / 实证

| CVE / 证据 | 实现 | 根因 |
|---|---|---|
| **CVE-2025-54939**（QUIC-LEAK，HIGH） | lsquic | 握手前路径对畸形/超限包分配内存未释放——传输参数解析与 Initial 处理同属无认证握手前路径，本 Skill TP-1~TP-5 是该路径的参数级系统展开 |
| 暂无参数校验独立 CVE | — | §18.2 校验分散在 §7.3/§18.2 多段，实现常只校验"能解析"不校验"值一致"——盲区条款 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、msquic、ngtcp2。
对比字段：TP-1~TP-5 各自的错误码与终止行为；重点对照"解析成功但值校验"是否独立存在。
误报排除：实现选择"忽略未知参数"（合规，RFC 允许）与"拒绝非法值"（必须）需区分；只标记 MUST 级校验缺失。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（传输参数字节 fuzz）、`tlsfuzzer-fuzz`（TLS 层扩展参数变异）
- 工具层（用什么打）：aioquic（自定义传输参数）、自写 TLS ClientHello 变异脚本
- 命中后动作：TP-4 成立 → 验证 CID 注入对路由层/重置令牌的影响链；TP-1~TP-3 → 按握手前路径崩溃面做 fuzz 扩展
