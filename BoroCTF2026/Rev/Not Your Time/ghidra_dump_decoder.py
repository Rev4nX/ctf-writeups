def parse_value(line):
    if "=" not in line:
        return None

    raw = line.split("=")[1].strip().rstrip(";")
    return int(raw, 16) if raw.startswith("0x") else int(raw)


def transform(x):
    return x ^ 0xff

with open("data.txt") as f:
    for line in f:
        v = parse_value(line)
        print(chr(transform(v)), end="")
