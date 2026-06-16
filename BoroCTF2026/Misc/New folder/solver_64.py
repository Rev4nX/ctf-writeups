import base64, os

files = os.listdir('ctf_chunks')
pairs = []
for f in files:
    idx = int(base64.b64decode(f, validate=False).decode().strip('\x00'))
    content = open(f'ctf_chunks/{f}', 'rb').read().strip()
    pairs.append((idx, content))

pairs.sort()
# only take files that have an actual letter before '40'
letters = ''.join(chr(c[0]) for _, c in pairs if len(c) == 3)
print(base64.b64decode(letters).decode())