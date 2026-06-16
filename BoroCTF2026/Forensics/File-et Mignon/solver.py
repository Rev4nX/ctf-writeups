import os

SEEK_DATA = 3
SEEK_HOLE = 4

f = os.open('filet_mignon.bin', os.O_RDONLY)
size = os.fstat(f).st_size
print(f'Logical size: {size:,} bytes ({size/1e12:.1f} TB)')

offset = 0
flag = ''
while offset < size:
    try:
        data_start = os.lseek(f, offset, SEEK_DATA)
    except OSError:
        break
    if data_start >= size:
        break
    try:
        hole_start = os.lseek(f, data_start, SEEK_HOLE)
    except OSError:
        hole_start = size
    os.lseek(f, data_start, 0)
    data = os.read(f, hole_start - data_start)
    printable = bytes(b for b in data if 32 <= b < 127).decode()
    flag += printable
    offset = hole_start

print('Flag:', flag)
os.close(f)