---
name: rfc9114-server-push-frame-rejection
description: 审计 HTTP/3 客户端/服务端是否严格拒绝服务端推送遗留帧——PUSH_PROMISE 与 MAX_PUSH_ID 收到必须按 H3_FRAME_UNEXPECTED 终止连接（RFC 9114 §7.2.5/§7.2.7），静默吞掉即协议错误义务缺失
rfc: RFC 9114 §7.2.5（PUSH_PROMISE）/ §7.2.7（MAX_PUSH_ID）/ §4.6（Server Push）
license: Apache-2.0
---

# RFC 9114 §7.2.5/§7.2.7 服务端推送遗留帧拒绝义务审计

## 1. 约束条款（原文出处）

RFC 9114 §7.2.5（原文）：
> A server MUST NOT send a PUSH_PROMISE frame. A client MUST treat the receipt of a PUSH_PROMISE frame as a connection error of type H3_FRAME_UNEXPECTED.
> If a PUSH_PROMISE frame is received on the control stream, the client MUST respond with a connection error of type H3_FRAME_UNEXPECTED.
> A client MUST NOT send a PUSH_PROMISE frame. A server MUST treat the receipt of a PUSH_PROMISE frame as a connection error of type H3_FRAME_UNEXPECTED.

RFC 9114 §7.2.7（原文）：
> A server MUST NOT send a MAX_PUSH_ID frame. A client MUST treat the receipt of a MAX_PUSH_ID frame as a connection error of type H3_FRAME_UNEXPECTED.
> Receipt of a MAX_PUSH_ID frame on any other stream [than the control stream] MUST be treated as a connection error of type H3_FRAME_UNEXPECTED.

RFC 9114 §4.6：HTTP/3 移除了服务端推送机制，§7.2 中 HTTP/2 遗留帧位（PRIORITY 0x2 / PING 0x6 / WINDOW_UPDATE 0x8 / CONTINUATION 0x9）收到即 H3_FRAME_UNEXPECTED（§7.2.8）。

核心模式一句话：**H3 把 H2 的推送和流控帧整体废弃，但保留了它们的类型码——这些类型码收到时必须炸连接，静默跳过等于给"已废弃语义"留了一条暗道，而暗道尽头是实现各自的理解。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| SP-1 | 服务端向客户端连接发送 PUSH_PROMISE 帧（载荷构造合法的 push ID + 压缩的请求头区块） | 客户端未以 H3_FRAME_UNEXPECTED 终止连接 → 违规（quic-go#5686 已实证该漏洞存在于 v0.60.0：静默丢弃） |
| SP-2 | 服务端向客户端连接发送 MAX_PUSH_ID 帧 | 客户端未终止 → 违规（与 SP-1 同根因，quic-go#5686 一并报告） |
| SP-3 | 客户端向服务端发送 PUSH_PROMISE 帧 | 服务端未以 H3_FRAME_UNEXPECTED 终止 → 违规 |
| SP-4 | 在 control stream 上收到 PUSH_PROMISE / 在非 control stream 上收到 MAX_PUSH_ID | 未按 H3_FRAME_UNEXPECTED 终止 → 违规 |
| SP-5 | 发送 H2 遗留保留帧（0x2 PRIORITY / 0x6 PING / 0x8 WINDOW_UPDATE / 0x9 CONTINUATION） | 未按 §7.2.8 以 H3_FRAME_UNEXPECTED 终止 → 违规（与已知正确的保留帧处理路径对照） |

判定方法：h3i 逐帧注入；对照实现：rama proxy 文档显示 H2 保留帧路径已正确区分，quic-go 同文件 0x2/0x6/0x8/0x9 正确 closeConn 而 0x5/0xd 漏判——同库内对照即可定位。

## 3. 攻击面猜想

- **已废弃语义的暗道复活**：SP-1 ——推送帧被静默吞掉看似无害，但若实现内部仍残留 push 处理代码路径（从 H2 移植），静默跳过 + 后续正常帧可能激活残留状态机
- **协议错误义务的系统性缺失**：SP-1~SP-5 全部落在"未知/不支持帧静默跳过"的兜底分支——该兜底分支被复用到多少其他 MUST 条款，是审计放大点
- **解析混淆垫脚石**：废弃帧载荷常被实现按未知帧"长度跳过"处理，长度字段解析错误即越界读/断言面

## 4. 关联历史 CVE / 实证

| 证据 | 实现 | 根因 |
|---|---|---|
| **quic-go issue #5686**（2026-06，确认于 v0.60.0，可能全版本） | quic-go http3/frames.go | PUSH_PROMISE(0x5) 与 MAX_PUSH_ID(0xd) 落入 payload-skip 兜底块被静默丢弃，而同为保留帧的 0x2/0x6/0x8/0x9 正确 closeConn——同一函数内的不一致处理是本条款审计的最佳入口证据 |
| erlang_quic 1.0.0 changelog | erlang_quic | "Server push lifecycle correctness (PUSH_PROMISE pairing, duplicate detection, MAX_PUSH_ID enforcement)" ——实现曾花整轮修复推送生命周期 |
| 暂无独立 CVE | — | 影响定级低-中（quic-go#5686 自评），但义务密集且集中暴露于同一兜底分支，按盲区条款处理 |

## 5. 差分验证方法

对照组：quic-go ≥ 修复版、nghttp3、erlang_quic ≥ 1.0.0。
对比字段：SP-1~SP-5 各自的终止行为；特别对照同一解析器内"正确处理的保留帧"与"漏判的推送帧"的代码路径差异。
误报排除：实现完全不编译推送相关代码且对 0x5/0xd 走统一 H2 保留帧错误路径属合规；只标记"静默跳过"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（废弃帧 + 后续正常帧组合序列）、`grammarinator-gen-fuzz`（帧类型语法生成）
- 工具层（用什么打）：h3i、aioquic
- 命中后动作：确认静默吞掉 → 探测残留 push 代码路径是否可被激活 → 评估与 CANCEL_PUSH/GOAWAY 交互的叠加面
