import numpy as np
from PIL import Image

img = Image.open("burn.png").convert("RGB")
arr = np.array(img)

# Wyciągnij tylko anomalie w kanale niebieskim
output = np.ones((800, 800), dtype=np.uint8) * 255
mask = arr[:, :, 2] < 254  # piksele gdzie blue < 254
output[mask] = 0

Image.fromarray(output).save("blue_only.png")
