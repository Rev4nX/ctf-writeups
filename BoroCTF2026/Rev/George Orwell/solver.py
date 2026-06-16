import re

ahk = """
secret := Chr(98) . Chr(111) . Chr(114) . Chr(111) . Chr(67) . Chr(84) . Chr(70) . Chr(123)
secret := secret . Chr(65) . Chr(72) . Chr(75) . Chr(95) . Chr(49) . Chr(115) . Chr(95)
secret := secret . Chr(108) . Chr(73) . Chr(115) . Chr(43) . Chr(101) . Chr(110) . Chr(105)
secret := secret . Chr(52) . Chr(103) . Chr(125)
"""

codes = re.findall(r'Chr\((\d+)\)', ahk)
print(''.join(chr(int(c)) for c in codes))