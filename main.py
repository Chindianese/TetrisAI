import screengrabber
import win32gui
import screengrabber
import ai
import save_load
# main loop

  
def main():    
    print('main')  
    game_borders = save_load.get_borders()
    print("press tab to start")     
    ai.start_ai(game_borders)  


   

print('starting') 
main()
print('shutting down')    