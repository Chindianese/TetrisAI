import cv2
import win32gui
import numpy as np
import sys
import linebreak
from desktopmagic.screengrab_win32 import (
    getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
    getRectAsImage, getDisplaysAsImages)

def find_borders(target_hwnd):  # get borders of tetris board
    left, top, right, bottom = win32gui.GetWindowRect(target_hwnd)
    # Capture an arbitrary rectangle of the virtual screen: (left, top, right, bottom)
    game_screen = getRectAsImage((left, top, right, bottom))
    print((left, top, right, bottom))
    game_screen = np.array(game_screen)
    #c
   
    height, width, channels = game_screen.shape
    min_val = 2
    max_val = 255
    board_color_max = np.array([max_val, max_val, max_val]) 
    board_color_min = np.array([min_val, min_val, min_val])
    mask = cv2.inRange(game_screen, board_color_min, board_color_max)
    #cv2.imshow("Screen", mask)
    # cv2.waitKey(-1)
    screen_top = -1
    screen_bottom = -1
    screen_left = -1

    for col in range(int((width/100*10)), width):
        color = mask[int(height / 2), col]
        if color > 0:  # found blank
            screen_left = col
            break

    for row in range(int(height/100*20), height):
        color = mask[height - row-1, screen_left + 10]
        if color > 0:  # found blank
            screen_bottom = row
            break
    for row in range(int(height/100*20), height):
        color = mask[row, screen_left + 10]
        if color > 0:  # found blank
            screen_top = row
            break

    print(f"top: {screen_top}")
    print(f"left: {screen_left}")
    print(f"bot: {screen_bottom}")
    screen_left += 2 # thickness offset
    tileSize = (height - screen_bottom - screen_top)/20
    # tileSizeB = (width - screen_left - screen_left)/10
    # print(tileSize,tileSizeB)
    #print(tileSize)
    game_borders = (left+screen_left, int(top+screen_top-tileSize*3), right-screen_left, bottom-screen_bottom)
    print(game_borders)
    # grab_screen(game_borders, True)
    #game_borders = (-814, 518, -624, 958)
    # grab_screen(game_borders, True)
    return game_borders

def grab_screen(game_borders, show = False):
    game_screen = getRectAsImage(game_borders)
    game_screen = np.array(game_screen)
    if show:
        cv2.imshow("cropped", game_screen)
        key = cv2.waitKey(-1)
    return game_screen

def save_to_file(mask):
    # saving to file for debugging
    np.set_printoptions(threshold=sys.maxsize)
    file = open("debug.txt", "w+")
    # Saving the array in a text file
    content = str(mask)
    file.write(content)
    file.close()
    linebreak.fix_line_break('debug.txt')