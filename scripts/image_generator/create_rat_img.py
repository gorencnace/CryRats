import numpy as np
import PIL.Image as pim
import cv2
from secrets import token_hex
from random import randint
import os

WRITE_PATH = "./images/generated/"

# Rats
RAT = "./images/rat.png"
RAT2 = "./images/rat2.png"
SKINNY = "./images/skinny-rat.png"
SKINNY2 = "./images/skinny-rat2.png"
FAT = "./images/fat-rat.png"
FAT2 = "./images/fat-rat2.png"

# Accessories
BUCKET_HAT = "./images/bucket-hat.png"
CHEF_HAT = "./images/chef-hat.png"
SANTA_HAT = "./images/santa-hat.png"
TOP_HAT = "./images/top-hat.png"
WITCH_HAT = "./images/witch-hat.png"
DREADLOCKS = "./images/dreadlocks.png"
GANGSTA = "./images/gangsta.png"

# Mappings
RATS_MAPPING = {0: RAT, 1: SKINNY, 2: FAT, 3: RAT2, 4: SKINNY2, 5: FAT2}
ACCESSORIES_MAPPING = {
    0: None,
    1: BUCKET_HAT,
    2: CHEF_HAT,
    3: DREADLOCKS,
    4: GANGSTA,
    5: SANTA_HAT,
    6: TOP_HAT,
    7: WITCH_HAT,
}

# colors BGR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = [0, 0, 255]
ORANGE_RED = [0, 69, 255]
GOLD = [0, 215, 255]

f = 5  # expantion factor


def generate_rat(
    token_id,
    size,
    accessory,
    rat_primary,
    rat_secondary,
    rat_tertiary,
    rat_eyes,
    background,
    accessory_primary,
    accessory_secondary,
):
    print("Generating image...")
    # read rat img
    rat_file_name = RATS_MAPPING[size]
    im = cv2.imread(rat_file_name, flags=cv2.IMREAD_COLOR)  # BGR format

    # new img
    img = np.zeros((64 * f, 64 * f, 3), dtype="uint8")
    # rat coloring
    for i in range(len(im)):
        for j in range(len(im[i])):
            b, g, r = im[i][j]
            for k in range(i * f, (i + 1) * f):
                for l in range(j * f, (j + 1) * f):
                    if b < 5 and g > 250 and 110 < r < 125:  # green
                        img[k][l] = background
                    elif b > 250 and g > 250 and r > 250:  # white
                        img[k][l] = rat_eyes
                    elif 40 < b < 50 and 45 < g < 60 and 70 < r < 85:  # brown
                        img[k][l] = rat_primary
                    elif b < 5 and 100 < g < 115 and r > 230:  # orange
                        img[k][l] = rat_secondary
                    elif 95 < b < 105 and g < 40 and r > 225:  # pink
                        img[k][l] = rat_tertiary
                    else:  # black
                        img[k][l] = BLACK

    # accessory coloring
    accessory_file_name = ACCESSORIES_MAPPING[accessory]
    if accessory_file_name:
        accessory = cv2.imread(accessory_file_name, flags=cv2.IMREAD_COLOR)

        for i in range(len(accessory)):
            for j in range(len(accessory[i])):
                b, g, r = accessory[i][j]
                for k in range(i * f, (i + 1) * f):
                    for l in range(j * f, (j + 1) * f):
                        if 95 < b < 105 and g < 40 and r > 225:  # pink
                            img[k][l] = accessory_primary
                        elif 40 < b < 50 and 45 < g < 60 and 70 < r < 85:  # brown
                            img[k][l] = accessory_secondary
                        elif b > 250 and g > 250 and r > 250:  # white
                            img[k][l] = WHITE
                        elif 50 < b < 70 and g > 225 and r > 245:  # yellow
                            img[k][l] = GOLD
                        elif b < 10 and g < 10 and r > 200:  # red
                            img[k][l] = RED
                        elif 205 < b < 220 and 180 < g < 200 and r < 10:  # blue
                            img[k][l] = ORANGE_RED
                        elif b < 10 and g < 10 and r < 10:  # black
                            img[k][l] = BLACK
    generated_path = f"{WRITE_PATH}{token_id}.png"
    cv2.imwrite(generated_path, img)
    print("Image saved!")
    return generated_path
