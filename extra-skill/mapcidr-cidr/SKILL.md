---
name: mapcidr-cidr
description: "Use mapcidr for CIDR range processing. Use when you need to expand a CIDR into an IP list, aggregate IPs into CIDRs, slice network segments, count IPs, or shuffle IP order. mapcidr is a CIDR processing tool from ProjectDiscovery with IPv4/IPv6 support. Any scenario involving CIDR computation, IP list processing, or network segment slicing should use this skill"
zh-signals: "使用 mapcidr 进行 CIDR 展开、聚合、切片与 IP 数量统计。信号:mapcidr,CIDR处理,网段展开,IP聚合,网段切片。"
when-to-use: >-
  Use when expanding CIDR ranges into IP lists, aggregating IPs into CIDRs, slicing subnets, counting addresses, or shuffling IP order for IPv4/IPv6 scanning workflows.
metadata:
  tags: "mapcidr,cidr,ip,network-segment,expansion,aggregation,slicing,IPv4,IPv6,projectdiscovery"
  category: "tool"
---

# mapcidr CIDR Range Processing Methodology

mapcidr is a CIDR processing tool from ProjectDiscovery. Core advantages: **expansion / aggregation / slicing / shuffling** + **dual-stack IPv4/IPv6** + **pipeline friendly**.

Project URL: https://github.com/projectdiscovery/mapcidr

## Basic Operations

```bash
# expand a CIDR into an IP list
echo 192.168.1.0/24 | mapcidr

# count the number of IPs
echo 10.0.0.0/16 | mapcidr -count

# aggregate an IP list into CIDRs
cat ips.txt | mapcidr -aggregate

# shuffle IP order (avoid triggering alerts during sequential scanning)
echo 192.168.1.0/24 | mapcidr -si

# skip the network address and broadcast address
echo 192.168.1.0/24 | mapcidr -skip-base -skip-broadcast
```

## Network Segment Slicing

```bash
# slice by host count (256 IPs per slice)
echo 10.0.0.0/16 | mapcidr -sbh 256

# slice by CIDR size (split into /24)
echo 10.0.0.0/16 | mapcidr -sbc 24

# distribute scanning across slices
echo 10.0.0.0/16 | mapcidr -sbc 24 | \
  while read cidr; do naabu -host "$cidr" -p 80,443 -silent; done
```

## Pipeline Integration

```bash
# CIDR expansion → port scanning
echo 10.0.0.0/24 | mapcidr -si | naabu -p 80,443 -silent

# deduplicate and aggregate IPs
cat scan_results.txt | mapcidr -aggregate

# filter IP ranges
echo 10.0.0.0/8 | mapcidr -fi 10.0.1.0/24
```
