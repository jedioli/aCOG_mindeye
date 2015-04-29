""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 multitetris.py

 ---------------------------------- (O)<< ----------------------------------------------
"""

import Tkinter as tk
import tkMessageBox
import tetris_base
import sys


class Tetris_Switcher(object):
    # used by root to switch between active games
    def __init__(self, parent, num_games):
        self.parent = parent    # usually root
        self.num_games = num_games
        self.game_list = []
        self.active_game = 0
        
    #    self.parent.bind("<space>", self.space_callback)
        self.parent.bind("<FocusIn>", self.switch_callback)
        
    #    self.after_id = self.parent.after(1, self.switch_focus)
    
    def start(self):
        tkMessageBox.showwarning(
            title="Controls",
            message="left:\t\tmove left\nright:\tmove right\nup:\t\trotate piece\nspace:\tswitch to next game\n\nCAREFUL! pieces may randomly rotate!",
            parent=self.parent
            )
        
        for x in range(num_games):
            window = tk.Toplevel(self.parent)
            window.title("Tetris Tk" + str(x+1))
            control = tetris_base.game_controller( window , self.parent)
            window.geometry('%dx%d+%d+%d' % (209,670, x*214, 28))
            self.game_list.append((window, control)) 
        
        self.parent.focus_force()
        self.parent.mainloop()    
    
    '''
    def switch_focus(self):
        print self.parent.focus_get()
        if self.parent.focus_get() == ".":  # meaning it's the root
            print "cool"
            self.active_game = (self.active_game + 1) % num_games
            window, control = self.game_list[self.active_game]
        #    print repr(window)
            window.lift()
            control.board.canvas.config(bg='mint cream')
            window.focus_force()
        #    return 'break'
        self.after_id = self.parent.after(1, self.switch_focus)
    '''
    
    def switch_callback(self, event):
    #    for game in self.game_list:
    #        game[1].board.canvas.config(bg="gray43")
        if not self.game_list:
            print "not yet started"
            return
        self.active_game = (self.active_game + 1) % num_games
        if self.active_game >= num_games:
            print "game out of bounds error"
            self.active_game = 0
        window, control = self.game_list[self.active_game]
    #    print repr(window)
        window.lift()
        control.board.canvas.config(bg='mint cream')
        window.focus_force()
        return 'break'
    



if __name__ == "__main__":
    
    print "please enter number of games"
    num_games = int(raw_input('num games? > '))
    
#    game_list = []
    
    root = tk.Tk()
    
    multi = Tetris_Switcher(root, num_games)
    multi.start()
    
    
    '''
    for x in range(num_games):
        window = tk.Toplevel(root)
        window.title("Tetris Tk" + str(x+1))
        game = BU_tetris_base.game_controller( window )
        window.geometry('%dx%d+%d+%d' % (209,470, x*214, 28))
        game_list.append((window, game))
    
    
    
    root.mainloop()
    '''
#    print root.tk.eval('wm stackorder '+str(root))
    
    '''
    for game in game_list:
        game[0].mainloop()
    '''
    
    print "ready"