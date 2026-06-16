# boroCTF 2026 — Silent Sentinel (Forensics, 100pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> We intercepted a packet capture containing a mix of modern station telemetry and an anomalous TCP file transfer. Analysts believe the rogue uplink successfully recovered an image of an iconic historical spacecraft where the crime must have taken place originally.  
> Flag Format: `boroCTF{satellite_name_with_underscores}`

## Files

- `space.pcap`

---

## Solution

### Step 1 — Extract TCP payload data

The pcap contains a TCP file transfer. TCP is a stream protocol — file data flows as raw bytes inside packet payloads. We extract the `Raw` layer from all TCP packets and concatenate them into one byte sequence:

```python
from scapy.all import rdpcap, TCP, Raw

pkts = rdpcap('space.pcap')
data = b''
for p in pkts:
    if p.haslayer(TCP) and p.haslayer(Raw):
        data += bytes(p[Raw])

with open('extracted', 'wb') as f:
    f.write(data)
print('Done, size:', len(data))
```

### Step 2 — Identify the extracted file

```bash
file extracted
```

Output:
```
extracted: JPEG image data, JFIF standard 1.01, ..., comment: "Satellite, Vanguard 1, Backup (A19761019000)."
```

The JPEG comment field contains the satellite name directly: **Vanguard 1**.

Vanguard 1 was the second US satellite launched into orbit (1958) and is the oldest man-made object still in orbit today.

---

## Flag

```
boroCTF{Vanguard_1}
```

---

## Key takeaways

- A pcap is a recording of network traffic — files transferred over TCP are embedded as raw bytes in packet payloads
- Extracting a TCP file transfer = concatenate the `Raw` payload of all TCP packets in order
- `tcpflow` may fail on non-Ethernet pcaps (datalink type 228 = raw IP) — use Scapy instead
- JPEG files can contain a comment field in their metadata — always check `file` output for extra info
- "Iconic historical spacecraft" + image in pcap = look at the image metadata, not just the image itself
