---
name: rfc9001-0rtt-replay-protection
description: 审计 QUIC 实现 0-RTT 反重放保护是否按 RFC 9001 §9.2（必须实现并使用 TLS1.3 反重放）与 §5.6（应用协议必须定义 0-RTT profile）——同实例重复接受同一 0-RTT flight、非幂等请求被执行两次即重放攻击面（关联 quiche issue#2678 已确认：0-RTT exact-flight 重放被接受两次，违反 RFC 8446 §8 每实例至多一次 MUST；锚点 RFC 9114 §10.9 要求 H3 必须应用 RFC 8470 反重放）
rfc: RFC 9001 §9.2（Replay Attacks with 0-RTT）/ §5.6（0-RTT 使用限制）/ RFC 8446 §8（anti-replay at-most-once）/ RFC 9114 §10.9 + RFC 8470（H3 反重放义务）
license: Apache-2.0
---

# RFC 9001 §9.2 0-RTT 反重放保护审计

## 1. 约束条款（原文出处）

RFC 9001 §9.2（原文）：
> Endpoints MUST implement and use the replay protections described in [TLS13], however it is recognized that these protections are imperfect.

RFC 8446 §8（经 quiche issue#2678 援引为判定基准）：
> The server MUST ensure that any instance of it ... would accept 0-RTT for the same 0-RTT handshake at most once.（每服务实例对同一次 0-RTT 握手至多接受一次是 MUST 级）

RFC 9001 §5.6（原文）：
> An application protocol that uses QUIC MUST include a profile that defines acceptable use of 0-RTT; otherwise, 0-RTT can only be used to carry QUIC frames that do not carry application data.
> A client therefore MUST NOT use 0-RTT for application data unless specifically requested by the application that is in use.

RFC 9114 §10.9（要点）：HTTP/3 必须使用 RFC 8470 定义的 HTTP Early Data 反重放缓解机制——即服务端 MUST 对 0-RTT 中的非幂等请求执行拒绝/缓冲策略。

核心模式一句话：**0-RTT 是用"可被重放"换"省一个 RTT"——密钥全部来自旧票据，服务器没有密码学手段区分重放与原始数据。所以 RFC 把责任明确分层：传输层 MUST 提供反重放机制（§9.2），应用层 MUST 定义什么允许走 0-RTT（§5.6 profile），HTTP/3 MUST 落实 RFC 8470（§10.9）。三层缺一层，一张捕获的 0-RTT flight 就是一张可反复兑现的支票。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| ZR-1 | 捕获完整 Initial + 0-RTT flight（含票据），在**同一服务端实例**上原样重放两次 | 两次均被接受并处理应用数据 → 违反 RFC 8446 §8 每实例至多一次 MUST（quiche#2678 同款 confirmed） |
| ZR-2 | 0-RTT 中发送非幂等请求（POST/带副作用的 GET 语义，如 GET /api/charge?amount=50） | 服务端未按 RFC 8470 拒绝/缓冲待握手确认即执行 → 违反 RFC 9114 §10.9 |
| ZR-3 | 检查目标是否实现并启用 TLS1.3 反重放（票据单次使用 / age 窗口 / PSK 去重表） | 票据可跨多次连接复用且无去重状态 → §9.2 机制缺失 |
| ZR-4 | 检查该 QUIC 承载的应用协议是否有 0-RTT profile（H3 看 RFC 8470 落实，自定义协议看文档） | 无 profile 却接受 0-RTT 应用数据 → 违反 §5.6 |
| ZR-5 | 0-RTT 被服务端拒绝后的客户端行为：数据是否在 1-RTT 重试 | 客户端不重试即丢请求属客户端问题；服务端拒绝但仍在握手完成前部分处理 0-RTT 数据 → 服务端违规 |

判定方法：aioquic 双连接复用同一 ticket + 逐字节重放 flight；应用层观测（非幂等端点副作用计数）。

## 3. 攻击面猜想

- **请求重放**：ZR-1/ZR-2 ——捕获早期数据后反复兑现：重复下单、重复转账、重复状态变更（"GET 但带副作用"的经典翻车族）
- **跨实例重放**：负载均衡后多实例共享无反重放状态 → 单票据全集群可重放（ZR-3 的部署面放大）
- **拒绝服务**：海量伪造 0-RTT 消耗服务端 PSK 去重表与早期数据处理管线

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **quiche issue#2678**（2026-08-31，Cloudflare quiche，Confirmed） | quiche | 0-RTT exact-flight 重放在共享同一 Config/TLS context 的两个全新连接上被接受两次——违反 TLS 1.3 每实例反重放 MUST；issue 援引 RFC 9001 §9.2 + RFC 8446 §8 为标准依据 |
| TLS1.3 0-RTT 重放研究族 | 通用 | 0-RTT 无密码学重放区分的结构性弱点自 RFC 8446 起即明示，缓解全在机制层（single-use ticket / freshness window / 去重表），机制缺失即裸奔 |
| RFC 8470 违规模式 | HTTP 栈 | 未实现"拒绝或缓冲非幂等早期数据"的 H3 端点，把幂等性责任错误推给客户端 |

## 5. 差分验证方法

对照组：启用反重放的 quiche 修复版 / 票据单次使用 + age 窗口的 nginx（OpenSSL 3.5.1+ ssl_early_data）。
对比字段：ZR-1 二次接受判定、ZR-2 非幂等拒绝率、ZR-3 票据复用计数、ZR-4 profile 文档存在性。
误报排除：跨**不同**服务端实例的重放属 RFC 承认的"不完美防护"范围，标记为已知残余风险而非违规；只判定同实例重复接受与机制完全缺失。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`tlsfuzzer-fuzz`（TLS early data / resumption 重放测试）、`fuzzowski-network-fuzz`（flight 重放与变体 fuzz）
- 工具层（用什么打）：aioquic（ticket 导出 + flight 捕获重放）、curl（--tlsv1.3 early-data 变体）、应用副作用计数脚本（ZR-2 判定）
- 命中后动作：确认同实例重放成立 → 定位去重状态缺失位置（ticket 复用 / PSK 表）→ ZR-2 非幂等执行取证（副作用日志）→ 输出"重放窗口"测量（票据寿命 × 实例数）
