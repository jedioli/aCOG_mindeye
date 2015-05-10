""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 multitetris.py

    Controller module for Multi-Tetris
        Handles switching between separate Tetris games
    Integrates with tetris_base.py
    
 DEPENDENCIES:
    Tkinter     -   Tk bindings for Python (included with Python)
 ---------------------------------- (O)<< ----------------------------------------------
"""

import Tkinter as tk
import tkMessageBox

import tetris_base
import sys

# Note: focus_force() is somewhat of an excessive function to use, as it doesn't respect
#   the native OS's windowing system. it works though. a better solution would be better.


class Tetris_Switcher(object):
    """controller for Multi-Tetris
    
    takes Tk.root as parent
    holds multiple games of Tetris
    controls active switching between games
    
    any number of games is theoretically possible, 
        though screen resolution restricts number that can be seen
    please do not move windows manually, as the switching order can be shuffled
    """
    def __init__(self, parent, num_games):
        self.parent = parent    # usually root
        self.num_games = num_games
        self.game_list = []
        self.active_game = num_games-1  # in order to start with game 0 after start()
        
        self.parent.bind("<FocusIn>", self.switch_callback)
        # used as a way to switch to the next game when passed focus by Tetris game,
        # and immediately send focus to next game
        
    
    def start(self):
        """start function
        
        displays controls (apologies if bad tab formatting)
        creates Toplevel windows to pass to individual Tetris games
        stores windows and game controllers
        """
        tkMessageBox.showwarning(
            title="Controls",
            message="left:\t\tmove left\nright:\tmove right\nup:\t\trotate piece\ndown:\tdrop faster\nspace:\tswitch to next game\n\nCAREFUL! pieces may randomly rotate!",
            parent=self.parent
            )
        
        for x in range(self.num_games):
            window = tk.Toplevel(self.parent)
            window.title("Tetris Tk" + str(x+1))
            control = tetris_base.game_controller( window , self.parent)
            window.geometry('%dx%d+%d+%d' % (209,670, x*214, 28))
            self.game_list.append((window, control)) 
        
        self.parent.focus_force()
        self.parent.mainloop()    
        
    
    def switch_callback(self, event):
        """callback function for game switch
        
        switches in L->R order
        works in conjunction with tetris_base space_callback 
            to highlight active game and darken idle games
        """
        if not self.game_list:
            print "not yet started"
            return
        self.active_game = (self.active_game + 1) % self.num_games
        if self.active_game >= self.num_games:
            print "game out of bounds error"
            self.active_game = 0
        window, control = self.game_list[self.active_game]
        window.lift()
        control.board.canvas.config(bg='mint cream')
        window.focus_force()
        return 'break'
    



if __name__ == "__main__":
    print "\nwelcome to Multi-Tetris!\nto quit, just close the Tk GUI windows or quit Tk\n"
    print "please enter number of games"
    how_many_games = int(raw_input('num games? > '))
    
    
    root = tk.Tk()
    
    multi = Tetris_Switcher(root, how_many_games)
    multi.start()
    