from scapy.all import rdpcap

pkts = rdpcap('chronos.pcap')
times = [float(p.time) for p in pkts]
delays = [round(times[i+1] - times[i], 6) for i in range(len(times)-1)]

# Mapowanie odstępów na bity
bits = ''.join('0' if round(d, 2) == 0.25 else '1' for d in delays)

# Sprawdź wszystkie 8 możliwych wyrównań bajtowych
for offset in range(8):
    chars = []
    for i in range(offset, len(bits) - 7, 8):
        chars.append(chr(int(bits[i:i+8], 2)))
    text = ''.join(chars)
    printable = sum(1 for c in text if 32 <= ord(c) < 127)
    if printable > len(chars) * 0.7:
        print(f'Offset {offset}: {text}')