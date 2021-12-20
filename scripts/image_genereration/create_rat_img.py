import numpy as np
import PIL.Image as pim
import cv2
from secrets import token_hex
from random import randint
import os

WRITE_PATH = "C:/Users/Nace/Documents/MAG2/CryRats/images/generated/"

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
RATS_MAPPING = {0: RAT, 1: FAT, 2: SKINNY, 3: RAT2, 4: FAT2, 5: SKINNY2}
ACCESSORIES_MAPPING = {
    0: None,
    1: BUCKET_HAT,
    2: CHEF_HAT,
    3: SANTA_HAT,
    4: TOP_HAT,
    5: WITCH_HAT,
    6: DREADLOCKS,
    7: GANGSTA,
}

# colors BGR
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [0, 0, 255]
ORANGE_RED = [0, 69, 255]
GOLD = [0, 215, 255]

f = 5  # expantion factor

for name in range(100):
    # random colors for rat
    RAT_COLOR_PRIMARY = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]  # [0, 0, 255]
    RAT_COLOR_SECONDARY = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]  # [255, 0, 0]
    RAT_COLOR_TERTIARY = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]  # [255, 255, 0]
    BACKGROUND = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]  # [0, 255, 0]
    RAT_EYES = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]  # [255, 255, 255]

    # random colors for accessory
    ACC_PRIMARY = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]
    ACC_SECONDARY = [
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
        np.uint8(int(token_hex(1), 16)),
    ]

    # read rat img
    rat_file_name = RATS_MAPPING[randint(0, len(RATS_MAPPING) - 1)]
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
                        img[k][l] = BACKGROUND
                    elif b > 250 and g > 250 and r > 250:  # white
                        img[k][l] = RAT_EYES
                    elif 40 < b < 50 and 45 < g < 60 and 70 < r < 85:  # brown
                        img[k][l] = RAT_COLOR_PRIMARY
                    elif b < 5 and 100 < g < 115 and r > 230:  # orange
                        img[k][l] = RAT_COLOR_SECONDARY
                    elif 95 < b < 105 and g < 40 and r > 225:  # pink
                        img[k][l] = RAT_COLOR_TERTIARY
                    else:  # black
                        img[k][l] = BLACK

    # accessory coloring
    accessory_file_name = ACCESSORIES_MAPPING[randint(0, len(ACCESSORIES_MAPPING) - 1)]
    if accessory_file_name:
        accessory = cv2.imread(accessory_file_name, flags=cv2.IMREAD_COLOR)

        for i in range(len(accessory)):
            for j in range(len(accessory[i])):
                b, g, r = accessory[i][j]
                for k in range(i * f, (i + 1) * f):
                    for l in range(j * f, (j + 1) * f):
                        if 95 < b < 105 and g < 40 and r > 225:  # pink
                            img[k][l] = ACC_PRIMARY
                        elif 40 < b < 50 and 45 < g < 60 and 70 < r < 85:  # brown
                            img[k][l] = ACC_SECONDARY
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

    cv2.imwrite(f"{WRITE_PATH}{name}.png", img)
