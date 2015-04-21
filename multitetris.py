""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 multitetris.py

 ---------------------------------- (O)<< ----------------------------------------------
"""

import Tkinter as tk
import tetris_base
import sys



if __name__ == "__main__":
    
    print "please enter number of games"
    num_games = int(raw_input('num games? > '))
    
    game_list = []
    
    for x in range(num_games):
        root = tk.Tk()
        root.title("Tetris Tk" + str(x+1))
        game = tetris_base.game_controller( root )
        root.geometry('%dx%d+%d+%d' % (209,470, x*214, 28))
        game_list.append((root, game))
    
    for game in game_list:
        game[0].mainloop()

    print "ready"