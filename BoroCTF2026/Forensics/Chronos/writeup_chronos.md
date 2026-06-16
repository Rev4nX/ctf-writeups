# boroCTF 2026 — Chronos (Forensics, 200pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> Would you rather possess the powers of Chronos, the God of Time or possess the powers of a bilingual?

## Files

- `chronos.pcap` — network packet capture, 312 TCP packets

---

## Reading the hints

- **"Chronos, God of Time"** → data is hidden in packet *timing*, not content
- **"Bilingual"** → bi (two) + lingual (language/digits) = **binary** — two symbols, zeros and ones

## Solution

### Step 1 — Examine the capture

```bash
tshark -r chronos.pcap | head -10
```

```
1   0.000000   10.10.10.5 → 192.168.1.20 TCP 40 4444 → 80 [SYN]
2   0.750000   10.10.10.5 → 192.168.1.20 TCP 40 [TCP Retransmission] ...
3   1.500000   10.10.10.5 → 192.168.1.20 TCP 40 [TCP Retransmission] ...
```

All 312 packets are **identical TCP SYN retransmissions** — same sender, receiver, size (40 bytes), zero payload. The only thing that varies is **arrival time**. This is a classic **timing covert channel**: data encoded in the rhythm of packet transmission, not in packet content.

### Step 2 — Identify the encoding

Inter-packet delays take exactly two values: **0.25s** and **0.75s**. Two values = two symbols = binary:

```
0.25s delay → bit 0
0.75s delay → bit 1
```

### Step 3 — Extract and decode

312 packets produce 311 inter-packet delays = 311 bits. 311 is not divisible by 8, so naively reading 8-bit groups from the start produces garbage. The key is to **try all 8 possible starting offsets**:

```python
from scapy.all import rdpcap

pkts = rdpcap('chronos.pcap')
times = [float(p.time) for p in pkts]
delays = [round(times[i+1] - times[i], 6) for i in range(len(times)-1)]

# Map delays to bits
bits = ''.join('0' if round(d, 2) == 0.25 else '1' for d in delays)

# Try all 8 byte-alignment offsets
for offset in range(8):
    chars = []
    for i in range(offset, len(bits) - 7, 8):
        chars.append(chr(int(bits[i:i+8], 2)))
    text = ''.join(chars)
    printable = sum(1 for c in text if 32 <= ord(c) < 127)
    if printable > len(chars) * 0.7:
        print(f'Offset {offset}: {text}')
```

Output:
```
Offset 7: oroCTF{c0mbobulat3_sp@gh3tti_nep0t1$m}
```

The missing leading `b` is at bit 6 (one bit before offset 7). The full flag is `boroCTF{c0mbobulat3_sp@gh3tti_nep0t1$m}`.

The author added 7 padding bits at the start of the bitstream to prevent trivial decoding from offset 0.

---

## Flag

```
boroCTF{c0mbobulat3_sp@gh3tti_nep0t1$m}
```

---

## Key takeaways

- **Timing covert channel** — data hidden in inter-packet delays instead of packet content. Invisible to content-based filters; the traffic looks like normal TCP retransmissions
- **"Bilingual" = binary** — "bi" (two) + "lingual" (language/digits). Two delay values (0.25s / 0.75s) encode two symbols (0/1)
- **Byte alignment offset** — when a bitstream doesn't start at a byte boundary, reading 8-bit groups from offset 0 produces garbage. Always try all 8 offsets. This is a common CTF trick
- **311 bits not divisible by 8** is a deliberate red herring — the real data starts at bit 7, giving 38 complete bytes (304 bits) from that point
- **Don't overcomplicate** — when you see only two delay values, the encoding is binary. The simple approach (two values = two bits) was correct from the start; only the offset was missing
