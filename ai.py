import screengrabber
import tetrisboard
import wait
import keyboard
import time
from pynput.keyboard import Key
import copy
def start_ai(game_borders):
    # ai loop
    keyboard.wait("tab")
    while True:
        score_list = []
        num_times_shift_list = []
        best_boards = []
        rot_board = []
        initial_score = 0
        for rotate_index in range(0, 4):
            loop_start = time.time()
            game_screen = screengrabber.grab_screen(game_borders, False)
            game_board = tetrisboard.screenshot_to_array(game_screen)
            if rotate_index == 0:
                edited = copy.deepcopy(game_board)
                for i in range(0, len(game_board)):
                    for j in range(0, len(game_board[i])):
                        if edited[i][j] == 2: 
                            edited[i][j] = 0
                initial_score = score_board(edited)
                print("Initial score: ", initial_score)
            # tetrisboard.print_board(game_board)           
            num_times_shift = tetrisboard.num_time_shift_left(game_board)
            shifted = tetrisboard.shift_moving_left_max(game_board, num_times_shift)
            repeat = False
            for board in rot_board:
                if board == shifted:
                    repeat = True
                    break
            if repeat:
                wait.key_press_wait(Key.up)
                continue
            rot_board.append(shifted)
            num_times_shift_list.append(num_times_shift)
            #gs_start = time.time()
            # Generate scores-----------------------------------------------------
            #dp = time.time()
            # drop time 0.13, now 0.013
            boards_list = tetrisboard.generate_drop_positions(game_board, num_times_shift, False)
            #print("drop", time.time() -  dp)
            #st = time.time()
            scores = score_all_boards(boards_list, initial_score) # score time 0.001
            #print("score", time.time() -  st)
            #print('gs', time.time() - gs_start)
            # loop_offset = time.time()
            (best_board_index, best_board_score) = select_best_board(scores)
            best_boards.append(boards_list[best_board_index])
            score_list.append((best_board_index, best_board_score))
            # rotate piece 
            wait.key_press_wait(Key.up)
            # print("loop", time.time() - loop_start)
            # print("offset", time.time() - loop_offset )
        best_rotation = select_best_rotation(score_list)
        # for rotate_index in range(0, len(best_boards)):
        #     print_board_with_score(best_boards[rotate_index], score_list[rotate_index],rotate_index, best_rotation)
        print_board_with_score(best_boards[best_rotation], score_list[best_rotation],best_rotation, best_rotation)
        
        # keyboard.wait("tab")
        execute_option(num_times_shift_list[best_rotation], score_list[best_rotation][0], best_rotation)

def print_board_with_score(board, score, rotate_index,best_rotation):
    title = "score board"
    if rotate_index == best_rotation:
        title = "best"
    tetrisboard.print_board(board, title)
    print("score",  score[1][0])
    print("height diff", score[1][1])
    print("clear", score[1][2])
    print("holes", score[1][3])
    print("highest", score[1][4])
def execute_option(num_times_shift, board_index, rotation):
    # rotate piece
    if rotation != 0:
        for t in range(0, rotation):
            wait.key_press_wait(Key.up)        
    shift_direction = num_times_shift - board_index
    if shift_direction > 0:
        for i in range(0, shift_direction):
             wait.key_press_wait(Key.left)   
    if shift_direction < 0 :
        for i in range(0, -shift_direction):
             wait.key_press_wait(Key.right)   
    wait.key_press_wait(Key.space) 

def select_best_rotation(score_list):
    max = score_list[0]
    max_index = 0
    for rotate_index in range(0,len(score_list)):
        if score_list[rotate_index][1] > max[1]:
            max = score_list[rotate_index]
            max_index = rotate_index
    return max_index


def select_best_board(scores):
    # Initialize maximum element
    max_index = 0
    max = scores[0]
    # Traverse array elements from second
    # and compare every element with
    # current max
    for i in range(1,  len(scores)):
        if scores[i] > max:
            max = scores[i]
            max_index = i
    return (max_index, scores[max_index])   

def score_all_boards(boards_list, initial_score):
    scores = []
    for i in range(0, len(boards_list)):
        score_info = score_board(boards_list[i], initial_score)
        scores.append(score_info)
    return scores


def score_board(game_board, initial_score = None): 
    if initial_score == None:
        initial_score = (0,0,0,0, 0)
    score = 0
    height_diff_multiplier = -1.2
    line_clear_multiplier = 0.7
    single_line_clear_multiplier = -0.6
    hole_multiplier =  -1.2
    highest_multiplier =  -0.4

    highest_block = height_difference_score(game_board) * height_diff_multiplier- initial_score[1]
    cls =  clear_line_score(game_board)
    if cls == 1:
        clear_line = cls * single_line_clear_multiplier - initial_score[2]
    else:
        clear_line = cls * line_clear_multiplier - initial_score[2]
    holes = hole_score(game_board) * hole_multiplier- initial_score[3]
    highest = highest_point_score(game_board) * highest_multiplier- initial_score[4]

    score += highest_block 
    score += clear_line
    score += holes
    score += highest
    return (score, highest_block, clear_line, holes, highest)

def highest_point_score(game_board):
    for row in range(0,23):
        for col in range(0,10): 
            if game_board[row][col] ==  2:
                return 23-row
    return 0


def height_difference_score(game_board):
    height_diff = 0
    prev = 0
    for col in range(0,10): 
        for row in range(0,24): # add one for floor
            if row == 23 or game_board[row][col] !=  0:
                if col == 0:
                    highest = 23 - row
                    prev = highest
                    break

                highest = 23 - row
                diff  = abs(highest - prev)
                diff /= 4 # reduce exponential
                height_diff += diff*diff
                prev = highest
                break
    return height_diff

def clear_line_score(game_board):
    lines = 0
    for row in range(0,23):
        for col in range(0,10):
            if game_board[row][col] ==  0:
                break
            if col == 9: # full line
                lines += 1
    return lines

def hole_score(game_board):
    num_holes = 0
    for col in range(0,10):
        has_block = False
        for row in range(0,23):
            if not has_block and game_board[row][col] !=  0:
                has_block = True
            if has_block and game_board[row][col] == 0:
                    num_holes += 1
    return num_holes