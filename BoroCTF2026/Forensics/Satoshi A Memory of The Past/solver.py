with open("data.txt") as file:
    for line in file:
        # wyciągnięcie wartości po "="
        raw = line.split("=")[1].strip().rstrip(";")

        # konwersja hex / dec
        if raw.startswith("0x"):
            value = int(raw, 16)
        else:
            value = int(raw)

        # XOR z 0x42
        flag_piece = value ^ 0x42

        # konwersja na znak ASCII
        character = chr(flag_piece)

        # wypisanie bez nowej linii
        print(character, end="")


# with open("data.txt") as file:
#     for line in file:
#         raw = line.split("=")[1].strip().rstrip(";")
#         value = int(raw, 16) if raw.startswith("0x") else int(raw)
#         print(chr(value ^ 0x42), end="")