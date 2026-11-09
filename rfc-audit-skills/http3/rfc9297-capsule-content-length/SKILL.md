---
name: rfc9297-capsule-content-length
description: 审计 HTTP Datagrams / Capsule Protocol 实现是否严格按 RFC 9297 §3.2/§3.3/§3.5——capsule 与 Content-Length 等头共存、截断 capsule、未知 capsule 类型处理错误即 HTTP 走私同族攻击面（同族：分享会未公开走私案例、CVE-2025-64702 模式）
rfc: RFC 9297 §2（HTTP Datagrams）/ §3.2（与 Content-Length 等头的互斥）/ §3.3（capsule 解析）/ §3.5（未知类型与中介行为）
license: Apache-2.0
---

# RFC 9297 §3 Capsule Protocol 互斥性与解析完备性审计

## 1. 约束条款（原文出处）

RFC 9297 §3.2（原文要点）：
> The Capsule Protocol MUST NOT be used with messages that contain Content-Length, Content-Type, or Transfer-Encoding header fields.
> A receiver that observes a violation MUST treat the HTTP message as malformed.

（HTTP/3 下 Content-Length 与 DATA 帧长度一致性本身另受 RFC 9114 §4.1.3 约束，见 `rfc9114-content-length-data-mismatch`。）

RFC 9297 §3.3：capsule 长度字段的冗余 varint 编码必须自洽（规范编码 + 非规范编码共存即视为畸形）；干净 FIN 上的截断 capsule（声明长度超过实际到达字节）必须视为 malformed。

RFC 9297 §3.5：未知 capsule 类型必须**静默丢弃**（跳过其声明长度）；中介未识别 Capsule-Protocol 协商时**不得**在 DATAGRAM 帧与 capsule 之间重编码转换；超大 capsule（理论上限 2^62-1）接收方应不缓冲直接丢弃。

RFC 9297 §2：HTTP Datagrams 只可与显式声明支持它们的请求/响应关联；未关联 datagram 的上下文出现 datagram 时，HTTP/3 下必须以 H3_DATAGRAM_ERROR（0x33）中止该流。

补充陷阱（实现层常见）：重复发送 `Capsule-Protocol` 头会被字段解析为 list，从而被**视为缺席**——capability 协商静默失效，进入"声明支持但未协商"的分裂状态。

核心模式一句话：**capsule 协议把"数据报语义"叠加在"字节流语义"之上，两套长度体系（capsule 内长 vs 外层 Content-Length/流结束）只要有一处不互斥、不自洽，就是经典的 HTTP 消息边界分裂走私。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| CP-1 | 发送同时携带 `Capsule-Protocol: ?1` 与 `Content-Length` 的响应，观察中间件与终端是否按 malformed 拒绝 | 任一侧接受并继续解析 → 走私面成立（与分享会未公开案例同族） |
| CP-2 | 发送冗余非规范 varint 编码的 capsule 长度（如 0x40 0x2A 表示 42），观察是否按畸形处理 | 接受非规范编码 → 解析分裂面 |
| CP-3 | 声明 capsule 长度后干净 FIN（实际字节 < 声明长度） | 未按 malformed 处理 → 截断走私面 |
| CP-4 | 注入未知 capsule 类型（含超大长度声明 2^62-1） | 未静默丢弃而是缓冲/崩溃 → 内存面；超大值被缓冲即 DoS 原语 |
| CP-5 | 在未协商 Capsule-Protocol 的连接上收发 DATAGRAM 帧 / capsule | 未中止流/未丢弃 → 关联违规 |
| CP-6 | 重复发送 Capsule-Protocol 头，观察协商状态 | 协商静默失效但数据面继续 → 分裂状态 |

判定方法：aioquic 自写对端构造 capsule 字节流；h3i 构造畸形 H3 消息；对照前后端两套解析器（如代理 vs 源站）的判定差异。

## 3. 攻击面猜想

- **HTTP 走私（消息边界分裂）**：CP-1/CP-3 ——前端按 Content-Length 切分、后端按 capsule 边界切分，注入的请求/响应被不同边界解释，与 CL.TE 走私同构
- **缓存投毒**：走私拆出的隐藏语义可注入到共享缓存的响应解析路径
- **内存耗尽**：CP-4 ——超大 capsule 长度被缓冲等待填满，单连接即可撑爆内存
- **能力协商失效导致的降级攻击**：CP-6 ——进入未定义协商状态后注入 datagram 语义

## 4. 关联历史 CVE

| CVE / 案例 | 实现 | 根因 |
|---|---|---|
| 分享会未公开案例（同族，CAP 协议走私） | 某网关实现 | capsule 与 Content-Length 共存时前后端解析分裂——与本 Skill CP-1 判定条件同构，验证本审计面的现实性 |
| **CVE-2025-64702**（同族模式参考） | quic-go QPACK 状态机 | 压缩/封装层状态机未强制容量约束——同属"叠加语义层的记账/边界义务未强制"模式 |

注：Capsule Protocol 2022 年才标准化，实现成熟度低、公开 CVE 极少——属"新协议 + 有明确 MUST"的高优先审计面。

## 5. 差分验证方法

对照组：quic-go、aioquic（两者 capsule 实现独立）；如可得再对照 nginx-quic / Cloudflare quiche。
对比字段：CP-1~CP-6 各自"拒绝/接受/崩溃"三态；前端代理与后端源站对同一份畸形消息的判定差异（走私成立的充要条件）。
误报排除：实现选择"见 Capsule-Protocol 与 Content-Length 共存即 400"属合规；只标记"接受并解析"与"两套解析器判定分裂"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`smuggler-desync`（消息边界分裂方法论直接复用）、`http2smugl-desync`（HTTP/2→HTTP/3 降级链）、`fuzzowski-network-fuzz`（capsule 字节流 fuzz）
- 工具层（用什么打）：aioquic、h3i
- 命中后动作：确认前后端解析判定分裂 → 构造端到端走私序列 → 评估缓存投毒/请求劫持可行性
