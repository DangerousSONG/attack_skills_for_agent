---
name: rfc9000-new-token-replay
description: 审计 QUIC 实现对 NEW_TOKEN 帧与令牌跨连接重放的防护是否按 RFC 9000 §19.7/§8.1.4——令牌单用约束、IP 绑定 MUST、重放未限即地址验证体系被绕过（盲区条款；格式自定 + MUST 分散的高 variance 面）
rfc: RFC 9000 §19.7（NEW_TOKEN 帧）/ §8.1.4（地址验证令牌完整性）
license: Apache-2.0
---

# RFC 9000 §19.7 NEW_TOKEN 生命周期与重放防护审计

## 1. 约束条款（原文出处）

RFC 9000 §8.1.4（原文）：
> Tokens sent in NEW_TOKEN frames MUST include information that allows the server to verify that the client IP address has not changed from when the token was issued... Attackers could replay tokens to use servers as amplifiers in DDoS attacks. To protect against such attacks, **servers MUST ensure that replay of tokens is prevented or limited**. Tokens that are provided in NEW_TOKEN frames need to be valid for longer but SHOULD NOT be accepted multiple times.

RFC 9000 §19.7（原文要点）：NEW_TOKEN 帧由服务端在握手后发送，向客户端发放可在**未来连接**中跳过地址验证的令牌；**客户端不得发送 NEW_TOKEN 帧**；令牌必须能区分于 Retry 令牌（"上下文区分符"）。

核心模式一句话：**NEW_TOKEN 是把地址验证成本摊到未来连接的性能优化——但每发出去一枚可重用令牌，就等于预签了一张"此地址可信"的远期支票，支票不记名、可转卖，兑现时服务端就要替伪造源地址的第三方买单。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| NT-1 | 客户端向服务端发送 NEW_TOKEN 帧 | 服务端未按 FRAME_ENCODING_ERROR / PROTOCOL_VIOLATION 终止 → 违规 |
| NT-2 | 建立连接 A 获得令牌，用同一令牌从**同一 IP** 发起连接 B1、B2……连续 N 次 | 全部被接受且均跳过地址验证 → 违反 SHOULD NOT 多次接受；出现任何一次接受且服务端无防重放状态 → 标记高风险 |
| NT-3 | 令牌跨 IP 重放（同令牌从另一源地址发起） | 被接受 → 违反 MUST 的 IP 绑定验证 |
| NT-4 | 令牌与 Retry 令牌混用：把 NEW_TOKEN 令牌放进收到 Retry 后的 Initial 回显位 | 被接受 → 上下文区分符缺失 → 违规 |
| NT-5 | 服务端发令牌的速率与总量观测：单连接可批量榨取多少枚有效令牌 | 无上限/无过期 → 重放面随令牌池规模线性放大，记录为缺口 |

判定方法：aioquic 双连接序列；令牌抓取后脚本化重放；服务端行为差分（带令牌/不带令牌 Initial 的响应差异）。

## 3. 攻击面猜想

- **地址验证体系旁路**：NT-2/NT-3 ——攻击者批量榨取令牌后配合源地址伪造，把服务端变成高倍率 UDP 放大器（解除 3 倍反放大限制的终局形态）
- **NAT 共享面**：§8.1.4 自述 IP 绑定在 NAT 场景"可能不足以保护共享 NAT 的其他主机"——令牌对 NAT 内其他主机同样有效，横向放大
- **令牌池污染**：NT-5 ——长期运行服务端积累的可重放令牌总量即攻击弹药库

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| 暂无 NEW_TOKEN 独立 CVE | — | 令牌格式由服务端自定义（RFC 刻意不规定格式），校验质量取决于各实现——"格式自定 + MUST 分散"是高 variance 盲区条款 |
| CVE-2023-49295 / CVE-2024-22189（同族模式） | quic-go 等 | 同属"协议义务（响应义务/记账义务）未强制即资源不对称"模式，地址验证义务旁路是其资源面变体 |
| RFC 9000 §8.1.4 NAT 自述 | 协议层 | 标准自身承认 IP 绑定验证在 NAT 下不充分——协议级残余风险，审计重点是实现是否在此之上再加约束 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、msquic、nginx-quic。
对比字段：NT-1 终止行为、NT-2 单用性、NT-3 IP 绑定、NT-4 上下文区分。
误报排除：实现选择"不发送 NEW_TOKEN"（完全不启用该优化）属合规最严形态；只标记"发令牌但无防重放/无 IP 绑定"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（地址验证旁路后的放大验证）、`fuzzowski-network-fuzz`（令牌字段 fuzz）
- 工具层（用什么打）：aioquic（令牌榨取与重放脚本）
- 命中后动作：NT-2/NT-3 成立 → 测量解除反放大限制后的放大比 → 评估作为反射放大器的可行性
