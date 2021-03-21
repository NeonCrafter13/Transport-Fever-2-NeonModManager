from PIL import Image
from freezeutils import find_data_file as f

import numpy as np


def invert_image(path):
    img = Image.open(path)

    img_array = np.array(img)

    I_max = 255

    img_array = I_max - img_array

    inverted_img = Image.fromarray(img_array)

    inverted_img.save(f(r"Image_negative.jpg"))
