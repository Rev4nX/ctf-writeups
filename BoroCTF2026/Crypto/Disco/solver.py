colors = [
    "#626f72",
    "#6f4354",
    "#467b6e",
    "#457633",
    "#725f6c",
    "#302465",
    "#5f596f",
    "#55345f",
    "#426540",
    "#747d00",
    "#000000",
    "#000000"
]

result = ''
for hex_color in colors:
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    result += chr(r) + chr(g) + chr(b)

print(result)