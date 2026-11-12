---
name: c2-beacon-analysis
description: "C2 Beacon configuration extraction and analysis. Use when capturing Cobalt Strike/Sliver/Havoc C2 framework beacon samples, memory dumps, or network traffic. Extracts key intelligence such as C2 addresses, communication protocols, Malleable Profiles, and Watermarks. Red-team perspective: understand how blue teams extract IOCs from beacons to improve C2 OPSEC"
zh-signals: "C2 Beacon 配置提取与分析。信号:C2,Beacon,Cobalt Strike,Sliver,配置提取,威胁狩猎"
when-to-use: "Use when capturing Cobalt Strike, Sliver, or Havoc beacon samples, memory dumps, or network traffic and needing to extract C2 configuration and IOCs."
metadata:
  tags: "c2,beacon,cobalt strike,sliver,havoc,malleable,watermark,configuration extraction,C2 analysis,threat hunting"
  category: "malware"
  mitre_attack: "T1071.001,T1573,T1095,T1572,T1090"
---

# C2 Beacon Configuration Extraction and Analysis

> **Red-team value**: understand what configuration a beacon leaks → customize the Malleable Profile → strengthen C2 OPSEC

## ⛔ Further Reading

- Manual CS Beacon decryption and TLV parsing → [references/cs-beacon-decrypt.md](references/cs-beacon-decrypt.md)
- Sliver/Havoc/Mythic implant analysis → [references/modern-c2-analysis.md](references/modern-c2-analysis.md)

---

## Phase 1: Beacon Type Identification

```
What type of sample was captured?
├─ PE/DLL file → Phase 2 (configuration extraction)
├─ Shellcode → Phase 2 (identify the stage first)
├─ Memory dump → Phase 3 (memory scanning)
├─ PCAP traffic → Phase 4 (traffic decoding)
└─ Process dump (MiniDump) → Phase 3
```

**Quick C2 framework identification:**
```bash
# YARA scan to identify the framework
yara -r c2_rules.yar sample.bin

# String signatures
strings sample.bin | grep -iE "(beacon|sleeptime|jitter|watermark|pipe)"   # CS
strings sample.bin | grep -iE "(sliver|implant|mtls|wg)"                   # Sliver
strings sample.bin | grep -iE "(havoc|demon|teamserver)"                   # Havoc
```

## Phase 2: Cobalt Strike Beacon Configuration Extraction

### Automated Extraction (preferred)

```python
from dissect.cobaltstrike.beacon import BeaconConfig
import json

configs = list(BeaconConfig.from_path("beacon.bin"))
for cfg in configs:
    settings = cfg.as_dict()
    # Key fields
    print(f"C2 Server:   {settings.get('SETTING_DOMAINS')}")
    print(f"Port:        {settings.get('SETTING_PORT')}")
    print(f"Sleep:       {settings.get('SETTING_SLEEPTIME')}ms")
    print(f"Jitter:      {settings.get('SETTING_JITTER')}%")
    print(f"User-Agent:  {settings.get('SETTING_USERAGENT')}")
    print(f"Watermark:   {settings.get('SETTING_WATERMARK')}")
    print(f"SpawnTo x64: {settings.get('SETTING_SPAWNTO_X64')}")
    print(f"PipeName:    {settings.get('SETTING_PIPENAME')}")
    print(f"BeaconType:  {settings.get('SETTING_BEACONTYPE')}")  # 0=HTTP,1=HTTPS,8=DNS
```

### Manual Decryption (when the automated tool fails)

```python
import struct

def decrypt_cs_config(data):
    """Manually XOR-decrypt the CS Beacon configuration"""
    # CS4: XOR key 0x2e, CS3: XOR key 0x69
    for xor_key in [0x2e, 0x69]:
        # Search for the encrypted magic: 0x0001 0x0002 (BeaconType, Short)
        magic = bytes([0x00 ^ xor_key, 0x01 ^ xor_key,
                       0x00 ^ xor_key, 0x02 ^ xor_key])
        offset = data.find(magic)
        if offset != -1:
            config_blob = bytes([b ^ xor_key for b in data[offset:offset+4096]])
            return parse_tlv(config_blob)
    return None

def parse_tlv(data):
    """Parse the TLV-formatted configuration"""
    FIELDS = {1:"BeaconType", 2:"Port", 3:"SleepTime", 5:"Jitter",
              8:"C2Server", 9:"UserAgent", 10:"PostURI", 26:"Watermark",
              36:"PipeName", 54:"SpawnTo_x64", 55:"SpawnTo_x86"}
    results = {}
    pos = 0
    while pos + 6 <= len(data):
        ftype = struct.unpack(">H", data[pos:pos+2])[0]
        dtype = struct.unpack(">H", data[pos+2:pos+4])[0]
        flen = struct.unpack(">H", data[pos+4:pos+6])[0]
        if ftype == 0: break
        val = data[pos+6:pos+6+flen]
        name = FIELDS.get(ftype, f"0x{ftype:04x}")
        if dtype == 3:  # string
            results[name] = val.rstrip(b'\x00').decode(errors='replace')
        elif dtype == 2:  # int
            results[name] = struct.unpack(">I", val[:4])[0]
        elif dtype == 1:  # short
            results[name] = struct.unpack(">H", val[:2])[0]
        pos += 6 + flen
    return results
```

## Phase 3: Memory Scanning Extraction

```bash
# Volatility3 scans the process memory
vol3 -f memory.dmp windows.memmap --pid <PID> --dump
# Extract from the dumped files using the Phase 2 method

# 1768.py (JPCERT) — dedicated CS config scanner
python3 1768.py -f memory.dmp

# CobaltStrikeParser scans memory
python3 parse_beacon_config.py memory.dmp
```

## Phase 4: Network Traffic Analysis

```
Derive network signatures from the beacon configuration:
├─ HTTP(S) Beacon → URI path + UA + Host header + heartbeat interval
├─ DNS Beacon → DNS query pattern + subdomain encoding scheme
├─ SMB Beacon → named pipe name
└─ TCP Beacon → port + protocol fingerprint
```

**Example generated detection signature:**
```
# Suricata
alert http any any -> any any (msg:"CS Beacon URI";
  content:"/api/v1/check"; http_uri;
  content:"Mozilla/5.0"; http_user_agent;
  threshold:type both, track by_src, count 5, seconds 300;
  sid:1000001; rev:1;)
```

## Phase 5: Red-Team OPSEC Reflection

Analysis results → your C2 should avoid the following exposures:

| Exposure Point | Countermeasure |
|--------|------|
| Default Watermark | Use a legitimate license or patch it out |
| Fixed User-Agent | Randomize it in the Malleable Profile |
| Fixed URI path | Mimic a real business API |
| Default named pipe `\\.\pipe\msagent_*` | Customize the pipe name |
| Default SpawnTo `rundll32.exe` | Change it to `svchost.exe` or another legitimate process |
| Fixed Sleep+Jitter | Increase jitter to 30%+ |
| Known XOR key (0x2e/0x69) | Use a sleep mask + heap encryption |

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| dissect.cobaltstrike | Python CS configuration parser |
| CobaltStrikeParser (S1) | CS Beacon configuration extraction |
| 1768.py (JPCERT) | CS scanner |
| BeaconEye | Real-time memory scanning for CS beacons |
| Volatility3 | Memory forensics |
| YARA | Signature matching |
