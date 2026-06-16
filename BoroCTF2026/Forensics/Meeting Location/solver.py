from scapy.all import rdpcap, ICMP

pkts = rdpcap(r'C:\Users\kajte\Projects\CTF\BoroCTF2026\Meeting Location\meeting.pcap')

chars = []
for p in pkts:
    if p.haslayer(ICMP) and p[ICMP].type == 8:
        payload = bytes(p[ICMP].payload)
        if len(payload) == 1:
            chars.append(payload.decode())

print(''.join(chars))