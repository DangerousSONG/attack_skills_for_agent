---
name: rfc9000-handshake-done-timing
description: 审计 QUIC 服务端对 HANDSHAKE_DONE 帧的发送时机与接收处理是否严格按 RFC 9000 §19.20 与 RFC 9001 §4.9.2——时序与密钥丢弃顺序错误可被恶意服务端/对端触发断言崩溃
rfc: RFC 9000 §19.20（HANDSHAKE_DONE）/ RFC 9001 §4.9.2（密钥丢弃）
license: Apache-2.0
---

# RFC 9000 §19.20 HANDSHAKE_DONE 时序与密钥丢弃审计

## 1. 约束条款（原文出处）

RFC 9000 §19.20（原文）：
> Servers MUST NOT send a HANDSHAKE_DONE frame before completing the handshake.
> A server MUST treat receipt of a HANDSHAKE_DONE frame as a connection error of type PROTOCOL_VIOLATION.

即两条义务：**发送方**（服务端）不得在握手完成前发送 HANDSHAKE_DONE；**接收方**（服务端角色）收到 HANDSHAKE_DONE 必须按 PROTOCOL_VIOLATION 终止连接。

RFC 9001 §4.9.2：握手确认后必须按既定顺序丢弃 Initial 密钥 / Handshake 密钥；丢弃时机的任何"提前"或"遗漏"都会破坏后续帧解密状态机。

核心模式一句话：**HANDSHAKE_DONE 是"握手已确认"的唯一信号帧，它的发送时机与收到后的密钥丢弃顺序共同构成握手期的资源生命周期——两条义务任何一条松掉，都可被远程触发崩溃。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| HD-1 | 作为恶意服务端，在握手尚未完成（客户端尚未确认服务端证书验证通过/密钥未就绪）时提前发送 HANDSHAKE_DONE，观察对端客户端行为 | 客户端进入断言/空指针崩溃 → 违反 §19.20 发送义务依赖的对端假设 |
| HD-2 | 作为客户端向服务端发送 HANDSHAKE_DONE 帧（合法客户端永不应发送），观察服务端 | 服务端未以 PROTOCOL_VIOLATION 终止连接 → 违反 §19.20 接收义务 |
| HD-3 | 在收到 HANDSHAKE_DONE 后，验证实现是否**立即**丢弃 Initial 密钥（修复 quic-go CVE-2025-59530 的做法），还是在应丢弃 Handshake 密钥的时机才丢弃 | 丢弃顺序与 §4.9.2 不符 → 密钥生命周期漏洞 |
| HD-4 | 握手期乱序注入 HANDSHAKE_DONE 重复帧 / 与 NewSessionTicket 交错的时序 | 状态机死锁或二次处理崩溃 → 违规 |

判定方法：aioquic 自写对端精确控制 HANDSHAKE_DONE 的发送时点；quic-go 调试日志观测密钥丢弃事件。

## 3. 攻击面猜想

- **远程断言崩溃（未认证）**：HD-1 ——恶意服务端在握手期即可打崩任意使用该客户端库的应用（quic-go 案例即 Solana Firedancer 野外被观测）
- **协议状态混乱**：HD-2 ——客户端伪造 HANDSHAKE_DONE 使服务端进入"握手已确认"状态，跳过了本应继续的握手校验
- **密钥生命周期错位**：HD-3 ——Initial 密钥存活过久意味着握手期伪造包有更长攻击窗口；丢弃过早则合法重传被误杀（可用性面）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2025-59530**（7.5 HIGH，CWE-617 Reachable Assertion） | quic-go < 0.49.0 / 0.54.1 / 0.55.0 | 客户端在握手未确认时收到服务端提前发送的 HANDSHAKE_DONE，触发断言崩溃；野外已观测到针对 Solana Firedancer 的攻击。修复 PR #5354：收到 HANDSHAKE_DONE 即丢弃 Initial 密钥，消除错误时序下的断言路径 |

注：HD-2/HD-4 属"有约束、暂无公开 CVE"的盲区条款——多数实现只修了崩溃路径（HD-1），未验证接收义务与乱序时序，值得定向审计。

## 5. 差分验证方法

对照组：quic-go ≥ 0.55.0（已修复）、msquic / ngtcp2。
对比字段：HD-1 是否崩溃、HD-2 是否返回 PROTOCOL_VIOLATION、HD-3 密钥丢弃事件时机、HD-4 乱序容忍度。
误报排除：实现选择更保守的"不立即断言而是记录并忽略"策略属合规；只标记"可达断言/未终止连接/密钥顺序错误"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（握手期帧时序 fuzz）、`grammarinator-gen-fuzz`（QUIC 握手帧序列语法生成；均在 tool-skills/）
- 工具层（用什么打）：aioquic（作为恶意服务端/客户端的帧级时序控制）
- 命中后动作：最小化触发帧序列 → 确认为可达断言或密钥生命周期错位 → 评估影响面（客户端库 → 所有下游应用）
