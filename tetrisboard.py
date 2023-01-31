import cv2
import numpy as np
from termcolor import colored
import screengrabber
import copy
import time
def screenshot_to_array(game_screen):
    #start = time.time()
    height, width, channels = game_screen.shape

    min_val = 30
    max_val = 255
    board_color_max = np.array([max_val, max_val, max_val])
    board_color_min = np.array([min_val, min_val, min_val])
    mask = cv2.inRange(game_screen, board_color_min, board_color_max)
    # screengrabber.save_to_file(mask) ## FOR DEBUGGING ONLYYYY dont be bobo and leave it here like me
    tile_size = width/10
    half_tile = tile_size/2
    #print("sub time", time.time() - start)

    rows, cols = (23, 10)
    game_board = [ [0]*cols for i in range(rows)]
    for row in range(0, rows):
        currentY = row*tile_size + half_tile
        #print('current row-------------------', int(currentY))
        for col in range(0, 10):
            currentX = col * tile_size + half_tile
            currentVal = mask[int(currentY), int(currentX)]
            board_val = 0
            if currentVal > 0:
                if row >= 0 and row <= 4:
                    board_val = 2
                else:
                    board_val = 1
            game_board[row][col] = board_val
            #print(int(currentX), currentVal)


    # print_board(game_board)
    return game_board

def print_board(game_board, title="board",start=0):
    print(title + "=============")
    # print(game_board)
    for row in range(start, 23):
        for col in range(10):
            number = game_board[row][col]
            if number == 0: 
                if row < 5:
                    print(colored('0 ', 'blue'), end='')
                else:
                    print(colored('0 ', 'grey'), end='')
            if number == 1:
                print(colored('0 ', 'white'), end='')
            if number == 2:
                print(colored('0 ', 'red'), end='')
        print('')


def num_time_shift_left(game_board, rows_to_check = 5): 
    shifted_board = copy.deepcopy(game_board)
    num_times_shift = 0
    found = False
    for i in range(0, len(game_board[0])):
        if found:
            break
        num_times_shift = i
        for j in range(0, min(rows_to_check, len(shifted_board))):
            if shifted_board[j][i] == 2:
                found = True
    # print(num_times_shift)
    return num_times_shift

def shift_moving_left_max(game_board, num_times_shift):
    shifted_board = copy.deepcopy(game_board)
    for i in range(0,5):
        row = shift_array_left(shifted_board[i], num_times_shift)    
        shifted_board[i] = row
    return shifted_board
def shift_moving_right(game_board):
    shifted_board = copy.deepcopy(game_board)
    for i in range(0,5):
        row = shift_array_right(shifted_board[i], 1)    
        shifted_board[i] = row

    return shifted_board

def shift_array_left(arr, num_times_shift):
    #print(arr)
    for i in range(0, num_times_shift):  
        for j in range(0, len(arr)-1):  
            #Shift element of array by one  
            arr[j] = arr[j+1];  
          
    arr[len(arr)-1] = 0;  
    #print(arr)
    return arr

def shift_array_right(arr, num_times_shift):
    #print(arr)
    for i in range(0, num_times_shift):  
        for j in range(0, len(arr)):  
            #Shift element of array by one  
            arr[len(arr)-1-j] = arr[len(arr)-1-j-1];  
           
    arr[0] = 0;  
    #print(arr)
    return arr
def raise_current(game_board):
    # print("raising")
    times_to_shift = 0
    found = False
    for row in range(0, 5):      
        if found:
            break    
        for col in range(0,10):
            if game_board[row][col] == 2:
                times_to_shift = row
                found = True
                break
    shifted_board = shift_up(game_board, times_to_shift)
    return shifted_board 

def drop_current(game_board):
    # print("dropping")
    times_to_drop = 50
    for row in range(0, 23):          
        for col in range(0,10):
            if game_board[row][col] == 2:
                for row_offset in range(row+1,24): # check below, addition loop for floor
                    if row_offset == 23: # bottom 
                        if row_offset-row-1 < times_to_drop:
                            times_to_drop = row_offset-row-1
                        break
                    if game_board[row_offset][col] == 2:
                        break
                    if game_board[row_offset][col] != 0: # hit block
                        if row_offset-row-1 < times_to_drop:
                            times_to_drop = row_offset-row-1
                            break
    shifted_board = shift_down(game_board, times_to_drop)
    return shifted_board 

def shift_up(game_board, num_times):
    shifted_board = copy.deepcopy(game_board)
    for row in range(0, 5):  
        for col in range(0,10):  
            if shifted_board[row][col] == 2:
                shifted_board[row][col] = 0
                shifted_board[row-num_times][col] = 2
    return shifted_board

def shift_down(game_board, num_times):
    shifted_board = copy.deepcopy(game_board)
    for row in range(0, 5):  
        for col in range(0,10):  
            if shifted_board[row][col] == 2:
                shifted_board[row][col] = 0
                shifted_board[row+num_times][col] = 2
    return shifted_board

def generate_drop_positions(game_board, num_times_shift, print_options = False):
    game_board = shift_moving_left_max(game_board, num_times_shift) # move current to the left
    if print_options:
        print_board(game_board, "left shifted") 
    # calc num output
    output = []
    num_output = 0
    for i in range(0, 10):
        num_output = i+1
        if game_board[0][9-i] == 2 or game_board[1][9-i] == 2 or game_board[2][9-i] == 2 or game_board[3][9-i] == 2 or game_board[4][9-i] == 2:
            break

    for i in range(0, num_output):
        #print_board(game_board)
        output.append(drop_current(game_board))
        if print_options:
            print_board(output[i], f"option {i}")    
        game_board = shift_moving_right(game_board)
    return output 