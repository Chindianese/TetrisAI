import screengrabber
import tetrisboard
import wait
import keyboard
import time
from pynput.keyboard import Key
import copy
import cv2
def start_ai(game_borders):
    # ai loop
    keyboard.wait("tab")
    switched_piece = False
    total_score = 0
    num_attempts = 0
    prev_score = 0
    total_loop = 0
    success = 0
    num_switch = 0
    while True:
        score_list = []
        num_times_shift_list = []
        best_boards =  []
        rot_board = []
        initial_score = 0
        skip = 0
        game_screen = screengrabber.grab_screen(game_borders, False)
        game_board_original = tetrisboard.screenshot_to_array(game_screen)
        game_board = copy.deepcopy(game_board_original)
        # tetrisboard.print_board("initial board", game_board)
        loop_start = time.time ()
        if(not check_current_exists(game_board)):
            print('continue')
            continue
        if len(game_board[0]) < 10:
            print('break')
            continue
        # time.sleep(0.5)
        for rotate_index in range(0, 4): 
            # tetrisboard.print_board(game_board)
            if rotate_index == 0: # blank board
                edited = copy.deepcopy(game_board)
                for i in range(0, len(game_board)):
                    for j in range(0, len(game_board[i])):
                        if edited[i][j] == 2: 
                            edited[i][j] = 0
                initial_score = score_board(edited)
                # print("Initial score: ", initial_score)
            # tetrisboard.print_board(game_board)           
            if len(game_board[0]) < 10:
                print('break')
                cv2.imshow("", game_screen)
                cv2.waitKey(-1)
            #tetrisboard.print_board(game_board, f"rotation: {rotate_index}")
            piece_row = current_piece_row(game_board)
            shifted_up = tetrisboard.raise_current(game_board, piece_row)
            num_times_shift = tetrisboard.num_time_shift_left(shifted_up)
            shifted = tetrisboard.shift_moving_left_max(shifted_up, num_times_shift, piece_row)
            # tetrisboard.print_board(shifted, f"rotation: {rotate_index}")
            repeat = False
            for board in rot_board:
                if board == shifted:
                    repeat = True
                    skip += 1
                    break
            if repeat:
                if rotate_index != 3:
                    rotate_piece(game_board, piece_row)
                continue
            rot_board.append(shifted)
            num_times_shift_list.append(num_times_shift)
            #gs_start = time.time()
            # Generate scores-----------------------------------------------------
            #dp = time.time()
            # drop time 0.13, now 0.013
            boards_list = tetrisboard.generate_drop_positions(shifted, num_times_shift, False)
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
            # wait.key_press_wait(Key.up)
            rotate_piece(game_board, piece_row)
            # print("offset", time.time() - loop_offset )
        best_rotation = select_best_rotation(score_list)
        current_score = score_list[best_rotation][1][0]            

        # print('sc', current_score)
    
        holes_score = score_list[best_rotation][1][3]
        # print('holes', holes_score)
        # print_board_with_score(best_boards[best_rotation], score_list[best_rotation],best_rotation, best_rotation)
        succ = "Success"
        if switched_piece:
            if current_score >= prev_score:
                success+= 1
            else:
                success = success
                succ = "Failure"
            print(succ + str(current_score) +"--" + "Switch success rate: ", success/num_switch)
        if not switched_piece and (current_score < -0.8 or (holes_score < 0 and current_score < 1 )):
            switch_piece()
            print('switching score: ', current_score)
            switched_piece = True
            # print('switching')
            prev_score = current_score
            num_switch += 1
            continue
        # for rotate_index in range(0, len(best_boards)):
        #     print_board_with_score(best_boards[rotate_index], score_list[rotate_index],rotate_index, best_rotation)
        
        # print_board_with_score(best_boards[best_rotation], score_list[best_rotation],best_rotation, best_rotation)
        total_score += current_score 
        num_attempts += 1
        loop_time = time.time() - loop_start
        total_loop +=loop_time
        #print('avg', total_score/num_attempts)    
        #print("current score", current_score)
        # print("loop avg",total_loop/num_attempts )
        #print("skip", skip)
       # print_board_with_score(best_boards[best_rotation], score_list[best_rotation],best_rotation, best_rotation)
        # keyboard.wait("tab") # ---------------------------------------------------------
        execute_option(num_times_shift_list[best_rotation], score_list[best_rotation][0], best_rotation)
        wait.wait(0.04, 0.045)
        switched_piece = False
def check_current_exists(arr):
    count = 0
    for row in range(0,23 ):
         for col in range(0,10):
            if arr[row][col] == 2:
                count +=  1
    return count == 4
             
def switch_piece(): 
    wait.key_press_wait(Key.shift_l)
    wait.wait(0.04, 0.045)
def rotate_piece(game_board, piece_row):
    top = game_board[max(piece_row-4, 0):piece_row+1]    
    rotated = list(zip(*top[::- 1]))
    for i in range(0, len(rotated)):
        rotated[i] = list(rotated[i])
    found  = False
    top_trimmed = []
    for i in range(len(rotated)):
        if found:
            break
        for j in range (len(rotated[i])):
            if rotated[i][j] == 2: # found piece
                found = True
                top_trimmed = rotated[i:i+5]
                break
    left_trimmed = []
    num_shift_left = tetrisboard.num_time_shift_left(top_trimmed)
    for i in range(0, len(top_trimmed)):
        left_trimmed.append(top_trimmed[i][num_shift_left:len(top_trimmed)])
    rev = [i[::-1] for i in left_trimmed]
    num_shift_right = tetrisboard.num_time_shift_left(rev)
    right_trimmed = []
    for i in range(0, len(left_trimmed)):
        end = len(left_trimmed[i])-num_shift_right
        val = left_trimmed[i][0:end]
        right_trimmed.append(val)
    trimmed = right_trimmed
    # remove prev piece
    for row in range(0,23):
        for col in range(0,10):
            if game_board[row][col] == 2:
                game_board[row][col] = 0
    # append
    formatted = []
    for i in range(0, len(trimmed)):
        row = copy.deepcopy(trimmed[i])
        if(len(trimmed[i]) == 1):
            for j in range(0, 5):
                row.insert(0,0)
            for j in range(0, 4):
                row.append(0)    
        elif(len(trimmed[i]) == 2):
            # if trimmed[0][0] == 0 and  trimmed[1][0] == 2 and trimmed[2][0] == 0:
            #     for j in range(0, 3):
            #         row.insert(0,0)
            #     for j in range(0, 5):
            #         row.append(0)
            # elif trimmed[0][0] == 2 and  trimmed[1][0] == 0 and trimmed[2][0] == 0:
            #     for j in range(0, 3):
            #         row.insert(0,0)
            #     for j in range(0, 5):
            #         row.append(0)    
            if (trimmed[0][0]+  trimmed[1][0] + trimmed[2][0]) == 2: # only one block
                for j in range(0, 3):
                    row.insert(0,0)
                for j in range(0, 5):
                    row.append(0)    
            else:
                for j in range(0, 4):
                    row.insert(0,0)
                for j in range(0, 4):
                    row.append(0)    
        elif(len(trimmed[i]) == 3):
            for j in range(0, 3):
                row.insert(0,0)
            for j in range(0, 4):
                row.append(0)   
        elif(len(trimmed[i])== 4):
            for j in range(0, 3):
                row.insert(0,0)
            for j in range(0, 3):
                row.append(0)     
        formatted.append(row)
    for i in range(0, len(formatted)):
        game_board[i] = formatted[i]
    return game_board

def current_piece_row(game_board):
    for row in range(0,23):
        for col in range(0,10):
            if game_board[22-row][col] == 2:
                return 22-row
    return -1

def print_board_with_score(board, score, rotate_index,best_rotation):
    title = "score board"
    if rotate_index == best_rotation:
        title = "best"
    tetrisboard.print_board(board, title)
    print("rot index",  best_rotation)
    print("score",  score[1][0])
    print("height diff", score[1][1])
    print("clear", score[1][2])
    print("holes", score[1][3])
    print("highest", score[1][4])
def execute_option(num_times_shift, board_index, rotation):
    # rotate piece
    if rotation != 0:
        for t in range(0, rotation):
            # print('rotate')
            wait.key_press_wait(Key.up)        
    shift_direction = num_times_shift - board_index
    # for i in range(0, 5):
    #     wait.key_press_wait(Key.left)   
    # for i in range(0, board_index):
    #     wait.key_press_wait(Key.right)   
    if shift_direction > 0:
        for i in range(0, shift_direction):
            # print('left')
            wait.key_press_wait(Key.left)   
    if shift_direction < 0 :
        for i in range(0, -shift_direction):
            # print('right')
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
    is_initial = False
    if initial_score == None:
        initial_score = (0,0,0,0,0,0)
        is_initial = True


 
    score = 0
    height_diff_multiplier = -0.7
    line_clear_multiplier = 2.2
    single_line_clear_multiplier = -1.2

    hole_multiplier =  -2.0
    highest_multiplier =  -0.2

    height_diff = height_difference_score(game_board) * height_diff_multiplier- initial_score[1]
    highest_point_raw = highest_block_raw(game_board)
    line_clear_penalty = 2
    if highest_point_raw >= 10:
        line_clear_penalty = 1
    if highest_point_raw >= 13:
        line_clear_penalty = 0

    cls =  clear_line_score(game_board)
    if cls <= line_clear_penalty and cls > 0:
        clear_line = (line_clear_penalty-cls+1) * single_line_clear_multiplier - initial_score[2]
    else:
        clear_line = cls * line_clear_multiplier - initial_score[2]
    holes = hole_score(game_board) * hole_multiplier- initial_score[3]
    highest_current = highest_point_score(game_board) 
    highest = (highest_current - highest_point_raw) * highest_multiplier

    score += height_diff 
    score += clear_line
    score += holes
    score += highest

    # if is_initial:
    #     print('ihigh', highest_point_raw)
    return (score, height_diff, clear_line, holes, highest)

def highest_block_raw(game_board):
    for row in range(0,23):
        for col in range(0,10): 
            if game_board[row][col] ==  1:
                return 23-row
    return 0

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