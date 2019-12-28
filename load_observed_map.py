import pyautogui
import pytesseract
from PIL import Image
import numpy as np
from time import sleep


def load_observed_map(MAGIC_NUMBER=(238, 130, 1682, 902), SIZE=(16, 30),
                      count=0, previous=None):
    print(' - LOADING IMAGE!')
    LEFT, UP, RIGHT, DOWN = MAGIC_NUMBER
    N_ROW, N_COL = SIZE
    PIXEL_W = (RIGHT - LEFT) // N_COL
    PIXEL_H = (DOWN - UP) // N_ROW
    CUT_W, CUT_H = np.linspace(LEFT, RIGHT, N_COL + 1)[:-1], np.linspace(UP, DOWN, N_ROW + 1)[:-1]
    PIXEL_CROP = int(PIXEL_H * 0.12)
    CENTER = (int(PIXEL_H * 0.2), int(PIXEL_W * 0.2))
    # print(PIXEL_CROP, CENTER)

    if previous is None:
        observed_map = - np.ones((N_ROW, N_COL), dtype=int)  # Unclicked: -1
    else:
        observed_map = previous

    sct = pyautogui.screenshot()
    sct.save(f'log/step_{count}.png')

    img = Image.open(f'log/step_{count}.png').convert('LA')
    for i, H in enumerate(CUT_H):
        # print(i)
        for j, W in enumerate(CUT_W):
            if observed_map[i, j] != -1:
                continue
            pixel = img.crop((W + PIXEL_CROP, H + PIXEL_CROP,
                              W + PIXEL_W - PIXEL_CROP, H + PIXEL_H - PIXEL_CROP))
            # pixel = img.crop((W, H,
            #                   W + PIXEL_W, H + PIXEL_H))
            # pixel.save(f'tst2/p_{i}_{j}.png')
            gray, _ = pixel.getpixel(CENTER)
            # print(i, j, gray)
            if 160 < gray < 170:
                val = -1
            else:
                try:
                    text = pytesseract.image_to_string(pixel,
                                                       config='--psm 10 -c tessedit_char_whitelist=0123456789')
                    val = int(text)
                except:
                    val = 0
            observed_map[i, j] = val
    return observed_map


# sleep(20)
# x = load_observed_map()
# print(x)
