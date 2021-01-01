from PIL import Image

import numpy as np
def invert_image(path):
    img = Image.open(path)

    img_arry = np.array(img)

    I_max = 255

    img_arry = I_max - img_arry

    inverted_img = Image.fromarray(img_arry)

    inverted_img.save(r"Image_negative.jpg")
