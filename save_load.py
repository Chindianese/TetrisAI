import pickle
def get_borders():
    print('getting borders')
    with open('borders.txt', 'rb') as f:
        game_borders = pickle.load(f)
        return game_borders  

def save_borders(game_borders):
    print('saving borders')
    d = game_borders
    with open('borders.txt', 'wb') as f:
        pickle.dump(d,f)      