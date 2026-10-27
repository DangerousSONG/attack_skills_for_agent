# ctf-osint — 详细参考（由 SKILL.md 拆分）

## Tor Relay Lookups

- `https://metrics.torproject.org/rs.html#simple/<FINGERPRINT>` -- check family, sort by "first seen". See web-and-dns.md.

## GitHub Repository Analysis

- Check issue comments, PR reviews, commit messages, wiki edits via `gh api`. See web-and-dns.md.

## Telegram Bot Investigation

- Find bot references in browser history, interact via `/start`, answer verification questions. See web-and-dns.md.

## FEC Political Donation Research

- FEC.gov for committee receipts; 501(c)(4) orgs obscure original funders. See web-and-dns.md.

## IP Geolocation

```bash
curl "http://ip-api.com/json/103.150.68.150"
```

See geolocation-and-media.md.

## Unicode Homoglyph Steganography

**Pattern:** Visually-identical Unicode characters from different blocks (Cyrillic, Greek, Math) encode binary data in social media posts. ASCII = 0, homoglyph = 1. Group bits into bytes for flag. See [social-media.md](social-media.md#unicode-homoglyph-steganography-on-bluesky-metactf-2026).

## BlueSky Public API

No auth needed. Endpoints: `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=...`, `app.bsky.actor.searchActors`, `app.bsky.feed.getAuthorFeed`. Check all replies to official posts. See [social-media.md](social-media.md#unicode-homoglyph-steganography-on-bluesky-metactf-2026).

## Fake Service Banner Detection

**Pattern:** Port appears open on a standard service port (22/SSH, 80/HTTP) but runs a fake service. `nmap -sV` or `nc host port` reveals the flag in the banner. Never trust port numbers alone -- always fingerprint the service. See [web-and-dns.md](web-and-dns.md#fake-service-banner-detection-via-fingerprinting-metactf-flash-2026).

## Shodan SSH Fingerprint Lookup

Search Shodan by SSH host key fingerprint to identify servers: `shodan search "fingerprint:AA:BB:CC:..."`. See [web-and-dns.md](web-and-dns.md#shodan-ssh-fingerprint-lookup-ekoparty-ctf-2016).

## Gaming Platform OSINT

Lookup usernames across gaming platforms (Steam, Xbox, PSN, MMOs) for character profiles, activity, and linked accounts. See [social-media.md](social-media.md#gaming-platform-osint--mmo-character-lookup-csaw-ctf-2016).

## Resources

- **Shodan** - Internet-connected devices
- **Censys** - Certificate and host search
- **VirusTotal** - File/URL reputation
- **WHOIS** - Domain registration
- **Wayback Machine** - Historical snapshots

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`geolocation-and-media.md`、`social-media.md`、`tools-mcp.md`、`web-and-dns.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
