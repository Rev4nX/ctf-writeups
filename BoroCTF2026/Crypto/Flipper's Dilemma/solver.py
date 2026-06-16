ciphertext = 'wzgzVASnS4|eE${J%`>h'
result = ''.join(chr(ord(c) ^ 0x15) for c in ciphertext)
print(result)