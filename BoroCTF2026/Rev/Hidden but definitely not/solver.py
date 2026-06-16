import re

text = open('dump.txt').read()
matches = re.findall(r'\[([^\]]+)\] = (0x[0-9a-f]+|\d+);', text)

data = {}
for idx, val in matches:
    i = int(idx, 16) if idx.startswith('0x') else int(idx)
    v = int(val, 16) if val.startswith('0x') else int(val)
    data[i] = v

for i in sorted(data):
    print(i, hex(data[i]), chr(data[i] ^ 7))

print('Flag:', ''.join(chr(data[i] ^ 7) for i in sorted(data)))