---
name: rfc9114-settings-frame-order
description: 审计 HTTP/3 实现对 SETTINGS 帧严格性是否按 RFC 9114 §7.2.1——SETTINGS 必须是每个 control stream 的第一帧，重复 SETTINGS 必须按 H3_FRAME_UNEXPECTED 连接错误处理
rfc: RFC 9114 §7.2.1（SETTINGS 帧）
license: Apache-2.0
---

# RFC 9114 §7.2.1 SETTINGS 帧顺序与唯一性审计

## 1. 约束条款（原文出处）

RFC 9114 §7.2.1（原文要点）：
> SETTINGS 帧**必须**是每个 control stream 上发送的第一个帧（The SETTINGS frame MUST be the first frame on the control stream）。
> 端点**不得**（MUST NOT）在 SETTINGS 之后再次发送 SETTINGS 帧；违反 MUST 的端点必须按 H3_FRAME_UNEXPECTED 类型的**连接错误**处理。
> 在收到 SETTINGS 帧之前，端点不得发送需要 SETTINGS 生效才可解释的请求/响应流量。

核心模式一句话：**SETTINGS 是 HTTP/3 控制流的"协议版本与能力协商锚点"，它的位置（第一帧）与唯一性（只出现一次）是所有后续语义解析的前置不变量——锚点松掉，后续一切解析都是未定义行为。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| SO-1 | 在 control stream 第一帧位置发送非 SETTINGS 帧（如 DATA/HEADERS/GREASE），观察对端 | 未按 H3_MISSING_SETTINGS 或 H3_FRAME_UNEXPECTED 终止连接 → 违规 |
| SO-2 | 正常 SETTINGS 之后再发送第二个 SETTINGS 帧（合法值或与合法值冲突的值各测一组） | 未按 H3_FRAME_UNEXPECTED 终止连接 → 违规；若接受第二个值 → 协商劫持面 |
| SO-3 | 发送空 SETTINGS（QPACK 动态表容量等关键项全缺省），观察对端是否按协商后的缺省值正确处理 | 缺省值处理与 RFC 不符 → 违规 |
| SO-4 | 在收到对方 SETTINGS 之前就发送依赖协商结果的帧（如大动态表编码的 HEADERS），观察是否被正确拒绝 | 未拒绝/未缓冲保护 → 违规 |
| SO-5 | 构造 control stream 上不完整的 SETTINGS（帧头声明长度 > 实际载荷，即流在 SETTINGS 中途结束） | 未按 H3_FRAME_ERROR 处理且存活 → 违规 |

判定方法：aioquic / quic-go 自写对端逐帧控制 control stream 内容；h3i 的 `send_frames_before_settings` 类场景。

## 3. 攻击面猜想

- **能力协商劫持**：SO-2 ——若实现接受第二个 SETTINGS，攻击者可覆盖 QPACK 动态表容量、H3_DATAGRAM 协商结果等能力位，导致后续解析全部错位
- **解析前置条件绕过**：SO-1/SO-4 ——在锚点建立前注入的帧可能被按"未初始化状态"解析，产生类型混淆或空指针路径
- **半开连接资源占用**：SO-5 ——不完整 SETTINGS 使对端无限等待 control stream 建立，配合多连接放大为资源耗尽

## 4. 关联历史 CVE

本条款**暂无公开 CVE**——属于典型的"有约束、无披露"盲区条款：RFC 明确要求、各实现也都声称支持，但"重复 SETTINGS 是否严格拒绝""非 SETTINGS 首帧是否严格终止"这两点在主流实现的测试覆盖中长期缺位。按本层方法论，这正是定向审计的高价值信号。

## 5. 差分验证方法

对照组：quic-go、nghttp3 / nghttp2 的 H3 端、Cloudflare quiche。
对比字段：SO-1~SO-5 各自的错误码与终止行为；特别关注"连接错误 vs 流错误"的层级是否一致。
误报排除：实现选择在收到非法 SETTINGS 序列后"记录并继续"但功能等价于终止的属合规；只标记"接受第二个 SETTINGS 生效"与"前置帧被解析"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（control stream 帧序列 fuzz）、`h2csmuggler-http2`（同族前置条件混淆思路的 H3 适配）
- 工具层（用什么打）：aioquic、h3i
- 命中后动作：确认第二个 SETTINGS 是否生效 → 若生效则评估协商劫持链；若只是未终止则记录为合规缺口
