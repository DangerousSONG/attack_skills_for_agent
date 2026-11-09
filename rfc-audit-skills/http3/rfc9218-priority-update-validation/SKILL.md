---
name: rfc9218-priority-update-validation
description: 审计 HTTP/3 实现对 PRIORITY_UPDATE 帧（RFC 9218 §7.2）的校验是否完备——帧位置、目标流类型、越限流 ID、推送流引用、优先级字段值解析错误即连接错误处理义务缺失
rfc: RFC 9218 §7（PRIORITY_UPDATE 帧）/ §4（urgency 与 incremental 参数）
license: Apache-2.0
---

# RFC 9218 §7 PRIORITY_UPDATE 帧校验完备性审计

## 1. 约束条款（原文出处）

RFC 9218 §7.2（原文要点）：
> The PRIORITY_UPDATE frame MUST be sent on the client control stream... Receiving a PRIORITY_UPDATE frame on a stream other than the client control stream MUST be treated as a connection error of type H3_FRAME_UNEXPECTED.
> The request-stream variant (0xF0700) MUST reference a request stream. If a server receives PRIORITY_UPDATE (0xF0700) for a stream ID that is not a request stream, this MUST be treated as a connection error of type H3_ID_ERROR. The stream ID MUST be within the client-initiated bidirectional stream limit. If a server receives PRIORITY_UPDATE (0xF0700) with a stream ID beyond the stream limits, this SHOULD be treated as a connection error of type H3_ID_ERROR.
> The push-stream variant (0xF0701) MUST reference a promised push stream. If a server receives PRIORITY_UPDATE (0xF0701) with a push ID greater than the maximum push ID or that has not yet been promised, this MUST be treated as a connection error of type H3_ID_ERROR.

RFC 9218 §4：Priority 字段值使用 HTTP Structured Fields 编码；urgency 取值 0-7，超出范围的值必须按协议忽略/处理（参数解析失败不得使连接进入未定义状态）。

核心模式一句话：**PRIORITY_UPDATE 把调度决策权交给对端，帧里引用的是"哪个流该被怎样调度"——引用校验（位置/类型/范围/存在性）任何一环松掉，就是把调度状态机的写入指针交到攻击者手里。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| PU-1 | 在 request stream / push stream / 服务端 control stream 上发送 PRIORITY_UPDATE（而非客户端 control stream） | 未按 H3_FRAME_UNEXPECTED 终止 → 违规 |
| PU-2 | 发送 0xF0700 且目标为服务端发起的流 ID / 非双向流 ID | 未按 H3_ID_ERROR 终止 → 违规 |
| PU-3 | 发送 0xF0700 且目标流 ID 超出当前并发流上限 | 未按 H3_ID_ERROR 处理（SHOULD 级，标记为缺口） → 违规 |
| PU-4 | 发送 0xF0701 且 push ID 未 promise / 超过 MAX_PUSH_ID | 未按 H3_ID_ERROR 终止 → 违规 |
| PU-5 | Priority Field Value 构造畸形 Structured Fields（urgency=99、嵌套乱序、非法字符）与超长字段值 | 解析崩溃 / 调度状态污染 / 连接卡死 → 违规；忽略畸形值 → 合规 |

判定方法：h3i 逐帧构造；aioquic 自写 control stream；对照调度日志观察目标流优先级是否被污染。

## 3. 攻击面猜想

- **调度优先级污染**：PU-2/PU-3 ——伪造高优先级引用使攻击者连接挤占带宽（低优先级饥饿 DoS 的反向面），或使关键流被饿死
- **解析崩溃面**：PU-5 ——Structured Fields 解析器实现差异大（RFC 8941 解析 corner case 多），畸形值触发断言/递归深度问题是 fuzz 高频命中区
- **连接错误义务缺失的共谋**：PU-1/PU-4 ——本应终止的违规被宽容，与其他帧处理瑕疵叠加成走私/混淆链的垫脚石

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| erlang_quic 1.0.0 changelog | erlang_quic | 明确修复 "Strict PRIORITY_UPDATE frame parsing per RFC 9218" ——说明主流实现在该帧解析上曾长期宽松 |
| 本条款暂无独立 CVE | — | RFC 9218 较新（2022），PRIORITY_UPDATE 属扩展帧，实现多按"未知帧忽略"路径兜底处理，恰好绕过全部 MUST——盲区条款 |

## 5. 差分验证方法

对照组：quic-go ≥ 0.60、nghttp3、erlang_quic ≥ 1.0.0。
对比字段：PU-1~PU-5 各自的错误码与终止行为；特别关注"扩展帧默认忽略"路径是否会吞掉 PRIORITY_UPDATE。
误报排除：实现不支持 RFC 9218（未在 SETTINGS 声明）时对 PRIORITY_UPDATE 按未知帧处理属合规；只标记"声明支持但校验缺失"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（control stream 帧序列 fuzz）、`dharma-grammar-fuzz`（Structured Fields 值语法生成）
- 工具层（用什么打）：h3i、aioquic
- 命中后动作：确认校验缺失 → 构造优先级污染序列评估调度公平性破坏 → 或确认解析崩溃路径最小化复现
