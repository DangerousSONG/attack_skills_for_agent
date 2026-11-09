---
name: rfc9114-goaway-drain-enforcement
description: 审计 HTTP/3 实现对 GOAWAY 优雅关闭语义是否严格按 RFC 9114 §5.2/§7.2.6——标识符单调性、收帧后拒新请求、无 GOAWAY 关闭的默认假设错误即连接生命周期与请求完整性漏洞（实证：quiche#2700、quic-go#5326、erlang_quic 1.0.0 修复；无独立 CVE）
rfc: RFC 9114 §5.2（Connection Shutdown）/ §7.2.6（GOAWAY 帧）
license: Apache-2.0
---

# RFC 9114 §5.2 GOAWAY 优雅关闭语义审计

## 1. 约束条款（原文出处）

RFC 9114 §5.2（原文要点）：
> Endpoints MUST NOT initiate new requests or promise new pushes on the connection after receipt of a GOAWAY frame from the peer.
> An endpoint MAY send multiple GOAWAY frames indicating different identifiers, but the identifier in each frame MUST NOT be greater than the identifier in any previous frame... Receiving a GOAWAY containing a larger identifier than previously received MUST be treated as a connection error of type H3_ID_ERROR.
> If a connection terminates without a GOAWAY frame, clients MUST assume that any request that was sent, whether in whole or in part, might have been processed.

RFC 9114 §7.2.6（原文要点）：
> A client MUST treat receipt of a GOAWAY frame containing a stream ID of any other type as a connection error of type H3_ID_ERROR.
> A client MUST treat a GOAWAY frame on a stream other than the control stream as a connection error of type H3_FRAME_UNEXPECTED.

核心模式一句话：**GOAWAY 是"哪些请求算数"的最终裁决帧，标识符单调性 + 收帧即拒新 + 异常关闭的保守默认三条义务共同保证请求既不丢也不重复执行——任何一条松掉，应用层就要面对请求丢失或重复处理的账。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| GA-1 | 正常握手后发送标识符为 N 的 GOAWAY，随后再发送标识符 N+k（更大）的 GOAWAY | 对端未按 H3_ID_ERROR 终止 → 违反单调性 MUST NOT |
| GA-2 | 收到服务端 GOAWAY（标识符 N）后，继续在标识符 ≥ N 的流上发送新请求，观察服务端是否拒绝（H3_REQUEST_REJECTED） | 服务端继续受理 → 违反"收帧后 MUST NOT 发起新请求"的对端义务依赖 |
| GA-3 | 发送 GOAWAY 至非 control stream 的流 / 载荷为推送方向标识符的服务端 GOAWAY | 对端未按 H3_FRAME_UNEXPECTED / H3_ID_ERROR 终止 → 违规 |
| GA-4 | 观察实现自身关闭行为：主动关闭连接时是否发送 GOAWAY，且标识符语义是否正确（已受理边界） | 无 GOAWAY 直接关 → 下游客户端进入"请求可能已执行"的不确定态（quiche#2700 实证模式） |
| GA-5 | 服务端发送 GOAWAY 后，是否显式取消（CANCEL/RESET）≥ 标识符的在途流（§5.2 SHOULD）并继续处理 < 标识符的流 | 在途流悬挂不处理也不取消 → 可用性面 |

判定方法：aioquic/h3i 构造多 GOAWAY 序列；对照实现关闭路径日志（是否发 GOAWAY、标识符取值）。

## 3. 攻击面猜想

- **请求重复执行 / 丢失**：GA-1/GA-4 ——标识符回退使客户端误判"请求未受理"而重试，实际已执行 → 非幂等操作重复扣款/下单；或反之丢失
- **优雅关闭劫持**：GA-2 ——在 GOAWAY 后受理新请求但随后无 GOAWAY 关闭，请求"可能已处理"态可被利用做事务不确定性攻击
- **连接生命周期资源悬挂**：GA-5 ——关闭过程中的在途流不取消，配合高频连接轮换可累积悬挂流状态

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| **quic-go issue #5686 同生态实证**（quiche#2700、quic-go#5326） | quiche / quic-go / erlang_quic | 关闭路径不发 GOAWAY 或 GOAWAY 后 drain 语义错误——erlang_quic 1.0.0 changelog 明确修复 "GOAWAY drain enforcement: reject new requests after a GOAWAY is sent or received" 与双端 GOAWAY 互答时误报 H3_ID_ERROR；quiche edge 万级请求后 H3_NO_ERROR 直接关连接无 GOAWAY |
| 本条款暂无独立 CVE | — | 属"多 MUST 但实现各自为政"的条款，合规 bug 密集但严重度分散，按盲区条款处理 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、nghttp3、erlang_quic ≥ 1.0.0。
对比字段：GA-1 是否 H3_ID_ERROR、GA-2 是否拒新请求、GA-4 关闭时 GOAWAY 存在性与标识符语义、GA-5 在途流处置。
误报排除：实现选择"收到递增 GOAWAY 时记录并采用最小值继续"且行为可证明等价于终止的属合规；只标记"接受递增""无 GOAWAY 关闭""收帧后受理新请求"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（控制流帧序列 fuzz）、`grammarinator-gen-fuzz`（GOAWAY 序列语法生成）
- 工具层（用什么打）：h3i、aioquic
- 命中后动作：确认标识符回退被接受 → 构造"请求已执行但客户端判定未执行"的重放场景 → 评估业务层影响（非幂等操作重复执行）
