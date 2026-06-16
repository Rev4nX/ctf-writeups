# boroCTF 2026 — Meeting Location (Forensics, 200pts)

**Author:** snzodiac  
**Category:** Forensics  

## Description

> I've got the network traffic from a well-known athlete. We don't know who the athlete is yet, but we'll address that after we confirm where they are meeting the other party. You know he will pay big bucks if we can get pictures of this athlete and why they are there for him. They're definitely talking in code about a secret meeting place in these packets. Take a look when you have a second. If you can figure out where they are heading, there's 200 boroPoints in it for you.  
> Note: the flag will NOT be wrapped with boroCTF{}

## Files

- `meeting.pcap`

---

## Solution

### Step 1 — Overview

Open the pcap in Wireshark or analyze with Scapy. The capture contains 1504 packets across multiple protocols: ICMP (324), TCP/HTTP (800), DNS (200), UDP (80).

### Step 2 — Identify the covert channel

The description says "talking in code." ICMP is the classic covert channel protocol — data can be hidden in ping payloads.

Extracting all unique ICMP echo request payloads reveals two types:
- **Noise:** long phrases like `routine maintenance ping sequence`, `latency measurement probe response`, `network performance monitor probe`
- **Signal:** single-character payloads: `W`, `W`, `F`, `z`, `X`, `0`, `1`, `h`, `c`, `m`, `l`, `u`, `Y`, `V`, `9`, `D`, `a`, `X`, `J`, `j`, `d`, `W`, `l`, `0`

### Step 3 — Extract and decode

Using Scapy to extract single-byte ICMP payloads in order:

```python
from scapy.all import rdpcap, ICMP

pkts = rdpcap('meeting.pcap')

chars = []
for p in pkts:
    if p.haslayer(ICMP) and p[ICMP].type == 8:  # echo request only
        payload = bytes(p[ICMP].payload)
        if len(payload) == 1:
            chars.append(payload.decode())

print(''.join(chars))
```

Output: `WWFzX01hcmluYV9DaXJjdWl0`

This is recognizable as base64 — alphanumeric characters only, length divisible by 4.

```bash
echo "WWFzX01hcmluYV9DaXJjdWl0" | base64 -d
```

Output: `Yas_Marina_Circuit`

### Step 4 — Identify the location

Yas Marina Circuit is the Formula 1 racing track in Abu Dhabi, UAE — hence the "well-known athlete" (F1 driver) and "pictures."

---

## Flag

```
boroCTF{Yas_Marina_Circuit}
```

---

## Key takeaways

- ICMP covert channel: data hidden in ping payloads, disguised by noise packets with legitimate-looking strings
- Single-byte payloads stand out from multi-word noise phrases — filter by payload length
- `strings` won't find this — it doesn't parse protocol structure. Use Scapy or Wireshark
- Base64 is recognizable on sight: alphanumeric + `/` + `+`, length divisible by 4
- **Challenge description bug:** the description explicitly stated "the flag will NOT be wrapped with boroCTF{}" — but the correct submission requires the wrapper. Always try both formats when a challenge specifies no wrapper, just in case.
