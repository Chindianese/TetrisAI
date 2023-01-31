import screengrabber
import win32gui
import save_load
targetWindow = "TETR.IO — Mozilla Firefox"
targetHWND = -1
topList = []


def enum_win(hwnd, result): 
    global targetHWND  
    if targetHWND >= 0: 
        return
    # print(hwnd)   
    win_text = win32gui.GetWindowText(hwnd) 
    # print(win_text)   
    if targetWindow in win_text:
        targetHWND = hwnd 
        print("found: ",win_text )  


win32gui.EnumWindows(enum_win, topList)
if targetHWND < 0:  
    print("failed to find")     
# time.sleep(1) 
game_borders = screengrabber.find_borders(targetHWND)  
save_load.save_borders(game_borders)
