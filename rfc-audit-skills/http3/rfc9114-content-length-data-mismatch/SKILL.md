---
name: rfc9114-content-length-data-mismatch
description: 审计 HTTP/3 目标是否违反 RFC 9114 §4.1.2 —— Content-Length 值必须等于收到的 DATA 帧长度之和；违规且被转发即存在 H3→H1 请求走私攻击面（关联 CVE-2026-33555 HAProxy）
rfc: RFC 9114 §4.1.2
license: Apache-2.0
---

# RFC 9114 §4.1.2 Content-Length 与 DATA 帧长度一致性审计

## 1. 约束条款（原文出处）

RFC 9114 §4.1.2（Malformed Requests and Responses）：

> A request or response that is defined as having content when it contains a Content-Length header field (Section 8.6 of [HTTP]) is malformed if the value of the Content-Length header field does not equal the sum of the DATA frame lengths received.

> Intermediaries that process HTTP requests or responses (i.e., any intermediary not acting as a tunnel) MUST NOT forward a malformed request or response. Malformed requests or responses that are detected MUST be treated as a stream error of type H3_MESSAGE_ERROR.

## 2. 违规判定条件

对目标（服务端 / H3 代理）发送以下三组探测，记录每种行为：

| 编号 | 探测 | 判定 |
|---|---|---|
| CL-1 | Content-Length = N，DATA 帧实际长度 ≠ N（多发/少发） | 正确行为：流被 H3_MESSAGE_ERROR 重置；违规：按原样接受并处理 |
| CL-2 | Content-Length = N，QUIC 流带 FIN 提前结束且 body 不足 N | 正确行为：判定 malformed；**重点测"裸 FIN 快速路径"是否跳过校验**（CVE-2026-33555 根因） |
| CL-3 | 通过代理转发到 H1 后端，CL 与 body 不一致的请求被原样转换 | 代理违反 MUST NOT forward → 确认走私面 |

判定方法：h3i（Cloudflare 开源 H3 测试工具，支持逐帧构造）、aioquic 自写客户端；观察 `RESET_STREAM` 的错误码是否为 `H3_MESSAGE_ERROR (0x0100)`。

## 3. 攻击面猜想

H3→H1 转换型代理在 body 长度校验上的任何宽容，都会把"前端 H3 解析"与"后端 H1 解析"分裂成两个判定主体 → **跨协议请求走私**：访问被 H1 前端规则拦截的后端资源、缓存投毒、会话固定。FIN 路径绕过（CL-2）意味着无需复杂帧序列，单连接即可触发。

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2026-33555** | HAProxy（HTTP/3 → HTTP/1） | 独立 QUIC FIN 走 standalone-FIN 快捷路径，跳过 `h3_check_body_size()` 的 RFC 9114 §4.1.2 校验，CL 不一致请求被转发出 H1 侧，跨协议走私。修复 commit `05a29544`（2026-03-18）在快捷路径补校验 |
| 参考：nginx/nginx#1043 | NGINX | 违反 §4.1.2：畸形 pseudo-header 请求未以 H3_MESSAGE_ERROR 关闭流（issue 状态：开放，未修复） |

## 5. 差分验证方法

对照组：quic-go ≥0.59.1、HAProxy ≥ 修复版（FIN 路径有校验）。
对比字段：CL-1/CL-2/CL-3 三组探测下目标是否返回 `H3_MESSAGE_ERROR`、是否转发、H1 后端收到的 body 是否与声明一致。
误报排除：部分实现对"never-has-content 响应允许非零 CL"（§4.1.2 第二段）是合规的，不要把响应用例误判为违规。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`smuggler-desync`（走私探测与利用）、`http2smugl-desync`（H2/H3 desync 变体；均在 tool-skills/）
- 工具层（用什么打）：h3i、aioquic（构造差分帧）、curl --http3（对照组）、Burp 类重放工具（注册表 Web 应用大类 272 个）
- 命中后动作：走私确认探针（访问仅后端可达的路径）→ 升级为缓存投毒/会话劫持利用链
