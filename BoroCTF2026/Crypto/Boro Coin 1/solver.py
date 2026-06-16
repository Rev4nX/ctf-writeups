from hashlib import sha256

# secp256k1 order
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def parse_der(sig_hex):
    sig = bytes.fromhex(sig_hex)
    # DER: 30 len 02 rlen r 02 slen s
    assert sig[0] == 0x30
    idx = 2
    assert sig[idx] == 0x02
    rlen = sig[idx+1]
    r = int.from_bytes(sig[idx+2:idx+2+rlen], 'big')
    idx = idx+2+rlen
    assert sig[idx] == 0x02
    slen = sig[idx+1]
    s = int.from_bytes(sig[idx+2:idx+2+slen], 'big')
    return r, s

def tx_hash(sender, recipient, amount):
    msg = f'{sender}:{recipient}:{amount}'
    return int.from_bytes(sha256(msg.encode()).digest(), 'big')

# Transaction 4: Suspect -> FranklinGothic, 21.68
r4, s4 = parse_der('304402202cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec702204b2f38c18c2a933f81112350ae048f0162feaaed599f827180944ea3203570de')
z4 = tx_hash('Suspect', 'FranklinGothic', '21.68')

# Transaction 19: Suspect -> ForeverFlames, 45.46
r19, s19 = parse_der('304402202cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec702207db2d815212aab6b986d0a403b724ad5fd57d2d9e826bf2893e29d9d179d59f3')
z19 = tx_hash('Suspect', 'ForeverFlames', '45.46')

print('r match:', r4 == r19)
print('r:', hex(r4))
print('z4:', hex(z4))
print('z19:', hex(z19))

# k = (z4 - z19) / (s4 - s19) mod n
k = ((z4 - z19) * pow(s4 - s19, -1, n)) % n
print('k:', hex(k))

# private key: d = (s4*k - z4) / r4 mod n
d = ((s4 * k - z4) * pow(r4, -1, n)) % n
print('private key:', hex(d)[2:])