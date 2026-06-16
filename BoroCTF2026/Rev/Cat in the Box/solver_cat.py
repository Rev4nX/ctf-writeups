key = b'ymweyc'  # 6 bajtów

# 25 surowych bajtów z DAT_00102010 (przepisanych z Ghidry)
prefix_enc = bytes([0x11, 0x19, 0x03, 0x15, 0x0a, 0x59, 0x56, 0x42,
                    0x11, 0x0c, 0x15, 0x06, 0x0a, 0x43, 0x14, 0x04,
                    0x0d, 0x01, 0x16, 0x15, 0x59, 0x08, 0x16, 0x06, 0x56])

# 4 surowe bajty z DAT_00102029
suffix_enc = bytes([0x57, 0x19, 0x0f, 0x11])

prefix = bytes([b ^ key[i % len(key)] for i, b in enumerate(prefix_enc)])
suffix = bytes([b ^ key[i % len(key)] for i, b in enumerate(suffix_enc)])

print(f'{prefix.decode()}{key.decode()}{suffix.decode()}')