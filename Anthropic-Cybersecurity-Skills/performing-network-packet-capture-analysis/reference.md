# performing-network-packet-capture-analysis — 详细参考（由 SKILL.md 拆分）

## Python PCAP Analysis

```python
from scapy.all import rdpcap, IP, TCP, UDP, DNS, DNSQR, Raw
import os
import sys
import json
from collections import defaultdict, Counter
from datetime import datetime


class PCAPForensicAnalyzer:
    """Forensic analysis of PCAP files using Scapy."""

    def __init__(self, pcap_path: str, output_dir: str):
        self.pcap_path = pcap_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.packets = rdpcap(pcap_path)

    def get_conversations(self) -> list:
        """Extract unique IP conversations with byte counts."""
        convos = defaultdict(lambda: {"packets": 0, "bytes": 0})
        for pkt in self.packets:
            if IP in pkt:
                key = tuple(sorted([pkt[IP].src, pkt[IP].dst]))
                convos[key]["packets"] += 1
                convos[key]["bytes"] += len(pkt)

        return [
            {"src": k[0], "dst": k[1], "packets": v["packets"], "bytes": v["bytes"]}
            for k, v in sorted(convos.items(), key=lambda x: x[1]["bytes"], reverse=True)
        ]

    def extract_dns_queries(self) -> list:
        """Extract all DNS queries from the capture."""
        queries = []
        for pkt in self.packets:
            if DNS in pkt and pkt[DNS].qr == 0 and DNSQR in pkt:
                queries.append({
                    "query": pkt[DNSQR].qname.decode(errors="replace").rstrip("."),
                    "type": pkt[DNSQR].qtype,
                    "src": pkt[IP].src if IP in pkt else "unknown"
                })
        return queries

    def detect_beaconing(self, threshold_seconds: float = 5.0) -> list:
        """Detect potential beaconing activity based on regular intervals."""
        ip_timestamps = defaultdict(list)
        for pkt in self.packets:
            if IP in pkt and TCP in pkt:
                key = (pkt[IP].src, pkt[IP].dst, pkt[TCP].dport)
                ip_timestamps[key].append(float(pkt.time))

        beacons = []
        for key, times in ip_timestamps.items():
            if len(times) < 5:
                continue
            deltas = [times[i+1] - times[i] for i in range(len(times)-1)]
            if deltas:
                avg_delta = sum(deltas) / len(deltas)
                variance = sum((d - avg_delta) ** 2 for d in deltas) / len(deltas)
                if variance < threshold_seconds and avg_delta > 1:
                    beacons.append({
                        "src": key[0], "dst": key[1], "port": key[2],
                        "avg_interval": round(avg_delta, 2),
                        "variance": round(variance, 4),
                        "connection_count": len(times)
                    })
        return sorted(beacons, key=lambda x: x["variance"])

    def get_protocol_distribution(self) -> dict:
        """Get protocol distribution statistics."""
        protocols = Counter()
        for pkt in self.packets:
            if TCP in pkt:
                protocols[f"TCP/{pkt[TCP].dport}"] += 1
            elif UDP in pkt:
                protocols[f"UDP/{pkt[UDP].dport}"] += 1
        return dict(protocols.most_common(50))

    def generate_report(self) -> str:
        """Generate comprehensive PCAP analysis report."""
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "pcap_file": self.pcap_path,
            "total_packets": len(self.packets),
            "conversations": self.get_conversations()[:50],
            "dns_queries": self.extract_dns_queries()[:200],
            "potential_beacons": self.detect_beaconing(),
            "protocol_distribution": self.get_protocol_distribution()
        }

        report_path = os.path.join(self.output_dir, "pcap_forensic_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"[*] Total packets: {report['total_packets']}")
        print(f"[*] Conversations: {len(report['conversations'])}")
        print(f"[*] DNS queries: {len(report['dns_queries'])}")
        print(f"[*] Potential beacons: {len(report['potential_beacons'])}")
        return report_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python process.py <pcap_file> <output_dir>")
        sys.exit(1)
    analyzer = PCAPForensicAnalyzer(sys.argv[1], sys.argv[2])
    analyzer.generate_report()


if __name__ == "__main__":
    main()
```

## References

- Wireshark Documentation: https://www.wireshark.org/docs/
- PCAP Analysis Mastery: https://insanecyber.com/mastering-pcap-review/
- SANS Network Forensics: https://www.sans.org/cyber-security-courses/network-forensics/
- Public PCAPs for Practice: https://www.netresec.com/?page=PcapFiles
