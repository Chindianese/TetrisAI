import random
import time
from pynput.keyboard import Key, Controller

def wait(min, max):
    time.sleep(random.uniform(min, max))

def key_press_wait(key):
    #print(key)
    keyboard = Controller()
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(random.uniform(0.04,0.05))
def key_press(key):
    #print(key)
    keyboard = Controller()
    keyboard.press(key)
    keyboard.release(key)