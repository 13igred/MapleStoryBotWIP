import random

import keyboard
import time


def KeyPress(key, delayTime):
    keyboard.press(key)
    time.sleep(delayTime)
    keyboard.release(key)


def DoubleKeyPress(key1, key2, delayTime):
    keypress = key1 + '+' + key2
    keyboard.press(keypress)
    time.sleep(delayTime)
    keyboard.release(keypress)


def Tap(key):
    keyboard.press_and_release(key)


def Jump():
    keyboard.press('up')
    keyboard.press_and_release('alt')
    a = random.uniform(0.1, 1)
    time.sleep(a)
    keyboard.press_and_release('alt')

