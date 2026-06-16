# boroCTF 2026 — Blackwall Protocol (Forensics, 200pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> We managed to intercept a raw, unfiltered braindance (BD) datastream right before the target crossed the Blackwall. The raw feed is heavily corrupted, but our netrunners swear there's something in the machine.

## Files

- `david_last_moments.bd` — disguised pcap file
- `bd_tuner.py` — Cyberpunk-themed viewer script with a key hint in comments

---

## Solution

### Step 1 — Identify the file type

The `.bd` extension is fictional (Braindance from Cyberpunk 2077). Always check actual content:

```bash
file david_last_moments.bd
# pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet)
```

It's a pcap. File extensions are just labels — `file` reads magic bytes and tells the truth.

### Step 2 — Read the hint in bd_tuner.py

```python
delay = random.choice([0.15, 0.65]) # Matches our timing channel delays!
```

The comment directly reveals the encoding: **timing covert channel** with two delay values. Same technique as the Chronos challenge.

### Step 3 — Analyze the capture

```bash
tshark -r david_last_moments.bd | head -20
```

14741 identical UDP packets. The only varying element is inter-packet timing. Three unique delay values appear:

```python
from scapy.all import rdpcap

pkts = rdpcap('david_last_moments.bd')
times = [float(p.time) for p in pkts]
delays = [round(times[i+1] - times[i], 6) for i in range(len(times)-1)]

# Unique delays: [0.0, 0.0001, 0.0006]
# 0.0    = noise/padding (14365 occurrences) — skip these
# 0.0001 = bit 0 (178 occurrences)
# 0.0006 = bit 1 (197 occurrences)
```

### Step 4 — Decode

```python
from scapy.all import rdpcap

pkts = rdpcap('david_last_moments.bd')
times = [float(p.time) for p in pkts]
delays = [round(times[i+1] - times[i], 6) for i in range(len(times)-1)]

# Map delays to bits, skip noise
bits = ''
for d in delays:
    rd = round(d, 4)
    if rd == 0.0001:
        bits += '0'
    elif rd == 0.0006:
        bits += '1'
    # rd == 0.0 → skip (noise)

# Try all 8 byte-alignment offsets
for offset in range(8):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(offset, len(bits)-7, 8)]
    text = ''.join(chars)
    printable = sum(1 for c in text if 32 <= ord(c) < 127)
    if printable > len(chars) * 0.8:
        print(f'Offset {offset}: {text}')
```

Output:
```
Offset 7: oroCTF{s4nd3v1st4n_gh0st_1n_th3_m4ch1n3_8f92a}
```

Missing leading `b` → full flag: `boroCTF{s4nd3v1st4n_gh0st_1n_th3_m4ch1n3_8f92a}`

---

## Flag

```
boroCTF{s4nd3v1st4n_gh0st_1n_th3_m4ch1n3_8f92a}
```

---

## Differences from Chronos

This challenge uses the same timing covert channel technique as Chronos, with three differences:

- **Disguised extension** — `.bd` instead of `.pcap`; `file` command reveals the truth
- **Faster timing** — 0.1ms/0.6ms instead of 250ms/750ms; same ratio, different scale
- **Noise packets** — 14365 zero-delay packets interspersed as padding; filter by skipping `delay == 0.0`

## Key takeaways

- **File extensions lie** — always run `file` first. `.bd`, `.dat`, `.bin` — anything can be a pcap
- **Hints in plain sight** — `bd_tuner.py` literally commented `# Matches our timing channel delays!` next to the two delay values
- **Noise filtering** — real covert channels often include padding/noise packets. Identify the meaningful delay values and skip everything else
- **Offset 7 again** — same as Chronos: the bitstream starts 7 bits before a byte boundary. When bit count isn't divisible by 8, always try all 8 offsets
