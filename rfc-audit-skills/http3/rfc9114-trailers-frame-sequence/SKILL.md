---
name: rfc9114-trailers-frame-sequence
description: 审计 HTTP/3 实现对 trailer 与多 HEADERS 帧序列的处理是否按 RFC 9114 §4.1/§4.2——trailing HEADERS 后的 DATA 即连接错误、trailer 与 Content-Length 一致性、重复响应头区块缺失校验即 H3 层消息走私面（盲区条款；nginx#1043 同生态；H2 trailer/CL 历史走私模式复刻）
rfc: RFC 9114 §4.1（HTTP 消息分帧）/ §4.2（请求/响应语义）/ RFC 9110 §8.6（Content-Length 与 trailer 一致性）
license: Apache-2.0
---

# RFC 9114 §4.1 Trailer 与帧序列合法性审计

## 1. 约束条款（原文出处）

RFC 9114 §4.1（原文要点）：
> Receipt of an invalid sequence of frames MUST be treated as a connection error of type H3_FRAME_UNEXPECTED. In particular, a DATA frame before any HEADERS frame, or a HEADERS or DATA frame after the trailing HEADERS frame, is considered invalid.

即 H3 消息的三个区块（初始 HEADERS → DATA → trailing HEADERS）各至多一次、顺序固定：trailing HEADERS 之后再出现任何 HEADERS/DATA 即连接错误。

RFC 9114 §4.1.2（字段区块约束）：trailing HEADERS 不得包含被禁止的伪头与连接级字段；RFC 9110 §8.6：trailer 的存在要求 Content-Length 与完整载荷一致（trailer 不得改变 CL 语义）。

核心模式一句话：**H3 用"帧序列"表达"消息的三个区块"——区块边界就是帧类型的合法顺序，第三个区块之后的任何帧都是消息边界外的字节，而消息边界外的字节就是走私的定义。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| TS-1 | 响应 trailing HEADERS 之后再发送 DATA 帧 | 未按 H3_FRAME_UNEXPECTED 终止 → 违规 |
| TS-2 | 响应出现第三个 HEADERS 帧（trailing 之后再 HEADERS） | 未终止 → 违规 |
| TS-3 | DATA 出现在任何 HEADERS 之前（请求与响应双向测试） | 未终止 → 违规 |
| TS-4 | trailing HEADERS 携带伪头字段（:status、:path 等）/ 连接级字段（connection、keep-alive） | 未按 malformed 处理 → 违规 |
| TS-5 | 携带 trailer 的响应 + 与 DATA 总和不一致的 Content-Length（CL 小于实际 / 大于实际各一组） | 未按 malformed 处理或中介转发 → 与 `rfc9114-content-length-data-mismatch` 叠加的走私面 |

判定方法：h3i 构造多区块帧序列（主力）；aioquic 自写响应流；对照前后端解析差异（H3 终端 vs H1 回源）。

## 3. 攻击面猜想

- **H3→H1 消息边界走私**：TS-1/TS-5 ——H3 端宽容接受 trailer 后 DATA，H1 回源按 CL 截断，边界分裂与第 1 批 CL 审计同构
- **解析分裂原语**：TS-3 ——无前导 HEADERS 的 DATA 若被某些实现解释为"隐含空头部区块"，与严格实现的差异即分歧点
- **trailer 语义注入**：TS-4 ——伪头进入 trailer 区块若被回源层重新解释，可伪造 :authority / :method 语义

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| nginx#1043（同生态，未修复） | nginx-quic | H3 字段区块 malformed 判定不完备——trailer 区块的字段约束与第 1 批伪头审计共享同一宽容解析面 |
| H2 历史模式（RFC 7540 §8.1.2 教训） | 多实现 | HTTP/2 时代 trailer/CONTINUATION 边界处理差异曾产生多起走私案例（如 CL 与 trailer 交互），H3 继承同一语义但换了一套帧机制——历史模式复刻面 |
| 暂无独立 CVE | — | 三个区块的顺序约束实现较直白，但 trailer 与 CL 一致性、trailer 伪头禁止属分散条款，组合测试覆盖少——盲区条款 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、nghttp3、nginx-quic。
对比字段：TS-1~TS-5 各自终止行为；重点对照"trailing HEADERS 后"与"任何区块后"的错误处理是否统一走 H3_FRAME_UNEXPECTED。
误报排除：实现选择拒绝所有 trailer（不显式支持第三个区块）属合规；只标记"接受 trailer 后数据"与"trailer 伪头被解析"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`smuggler-desync`（边界分裂利用）、`http2smugl-desync`（H2/H3 降级链）、`fuzzowski-network-fuzz`（帧序列 fuzz）
- 工具层（用什么打）：h3i（区块序列构造主力）、aioquic
- 命中后动作：TS-1/TS-5 分裂确认 → 构造端到端走私探针 → 评估缓存投毒/请求劫持链
