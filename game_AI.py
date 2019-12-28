from cal_expectation import strategy
from load_observed_map import load_observed_map
import win32api, win32con
from time import sleep
import numpy as np


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(0.1)


MAGIC_NUMBER = (238, 130, 1682, 902)
LEFT, UP, RIGHT, DOWN = MAGIC_NUMBER
N_COL, N_ROW = 30, 16
CUT_W, CUT_H = np.linspace(LEFT, RIGHT, N_COL + 1)[:-1], np.linspace(UP, DOWN, N_ROW + 1)[:-1]
N_MINE = 99
SIZE = (16, 30)
C = 0
exp = None
observed = None
ppx, ppy = None, None

sleep(5)
while True:
    print('STEP:', C)
    if C == 0:
        x, y = 8, 15
    else:
        observed = load_observed_map(MAGIC_NUMBER, SIZE, C, observed)
        (x, y), exp = strategy(observed, N_MINE, exp)
    print(' - CLICK:', x, y)
    px, py = int(CUT_W[y] + 10), int(CUT_H[x] + 10)
    if (px, py) == (ppx, ppy):
        break
    # print(px, py)
    click(px, py)
    ppx, ppy = px, py
    C += 1

