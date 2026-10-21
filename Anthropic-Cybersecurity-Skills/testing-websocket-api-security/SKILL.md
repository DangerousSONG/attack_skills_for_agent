---
name: testing-websocket-api-security
description: Tests WebSocket API implementations for missing upgrade-handshake authentication,
when-to-use: Tests WebSocket API implementations for missing upgrade-handshake authentication,
  Cross-Site WebSocket Hijacking (CSWSH), message injection, insufficient input validation,
  message-flooding DoS, and information leakage, using Burp Suite's WebSocket interception
  and the wscat CLI to craft malicious payloads. Use for real-time API penetration testing
  or CSWSH/authorization-bypass assessments on WebSocket channels.
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- websocket
- cswsh
- real-time
- injection
- authentication
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1552.001
- T1055
- T1059
---
# Testing WebSocket API Security

## When to Use

- Assessing real-time communication APIs that use WebSocket (ws://) or Secure WebSocket (wss://) protocols
- Testing for Cross-Site WebSocket Hijacking (CSWSH) where an attacker's page connects to a legitimate WebSocket server
- Evaluating authentication and authorization enforcement on WebSocket connections and messages
- Testing input validation on WebSocket message payloads for injection vulnerabilities
- Assessing WebSocket implementations for denial-of-service through message flooding or oversized frames

**Do not use** without written authorization. WebSocket testing may disrupt real-time services and affect other connected users.

## Prerequisites

- Written authorization specifying the WebSocket endpoint and testing scope
- Burp Suite Professional with WebSocket interception capability
- Python 3.10+ with `websockets` and `asyncio` libraries
- Browser developer tools for observing WebSocket handshakes and frames
- wscat CLI tool for manual WebSocket interaction: `npm install -g wscat`
- Knowledge of the WebSocket subprotocol in use (JSON-RPC, STOMP, custom)

## Workflow

### Step 1: WebSocket Endpoint Discovery and Handshake Analysis

```python
import asyncio
import websockets
import json
import ssl
import time

WS_URL = "wss://target-api.example.com/ws"
AUTH_TOKEN = "Bearer <token>"

# Capture and analyze the WebSocket handshake
async def analyze_handshake():
    """Analyze WebSocket upgrade request and response headers."""
    try:
        async with websockets.connect(
            WS_URL,
            extra_headers={"Authorization": AUTH_TOKEN},
            ssl=ssl.create_default_context()
        ) as ws:
            print(f"Connected to: {WS_URL}")
            print(f"Protocol: {ws.subprotocol}")
            print(f"Extensions: {ws.extensions}")

            # Send a test message
            test_msg = json.dumps({"type": "ping"})
            await ws.send(test_msg)
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print(f"Server response: {response}")

            return True
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Connection rejected: {e.status_code}")
        return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

asyncio.run(analyze_handshake())
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
