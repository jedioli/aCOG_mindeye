""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 multitetris_adapt.py

    Controller module for Multi-Tetris_adapt
        Handles switching between separate Tetris games
        Includes dynamic showing ("adding") and hiding ("removing") games
    Integrates with tetris_base.py
    
 DEPENDENCIES:
    Tkinter     -   Tk bindings for Python (included with Python)
    

 STILL IN PRE-ALPHA STAGES!
    "ghost" pieces float in window after game is removed and re-added
    rapid add/remove of games loses user control, no window has focus
        FIXED! forgot to give focus back to current game.
    rapid add/remove of games or adding too many games can crash program
 ---------------------------------- (O)<< ----------------------------------------------
"""

import Tkinter as tk
import tkMessageBox
import tetris_base_adapt
import sys

# RESOURCES:
#   http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/

# Note: focus_force() is somewhat of an excessive function to use, as it doesn't respect
#   the native OS's windowing system. it works though. a better solution would be better.


class Tetris_Switcher(object):
    """controller for Multi-Tetris_adapt
    
    takes Tk.root as parent
    holds multiple games of Tetris
    controls active switching between games
    
    also allows for dynamic showing/hiding games
    future work: place show/hide in externally callable functions, no key presses
    
    creates 6 games by default, starts player with 3
    please do not move windows manually, as the switching order can be shuffled
    """
    def __init__(self, parent, num_games=6):
        self.parent = parent    # usually root
        self.num_games = num_games
        self.game_list = {}         # indexed as {game_index : (window, game_control)}
        self.hidden_games = {}      # indexed as {game_index :  window}
        self.active_game = 0
        
        self.parent.bind("<FocusIn>", self.switch_callback)
        # used as a way to switch to the next game when passed focus by Tetris game,
        # and immediately send focus to next game
    
    def start(self):
        """start function
        
        displays controls (apologies if bad tab formatting)
        creates Toplevel windows to pass to individual Tetris games
        stores windows and game controllers in game list and dict
        """
        tkMessageBox.showwarning(
            title="Controls",
            message="left:\t\tmove left\nright:\tmove right\nup:\t\trotate piece\nspace:\tswitch to next game\n-:\t\tremove rightmost game\n= (+):\tadd game to right\n\nCAREFUL! pieces may randomly rotate!",
            parent=self.parent
            )
        
        for x in range(self.num_games):
            window = tk.Toplevel(self.parent)
            window.title("Tetris Tk" + str(x+1))
            control = tetris_base_adapt.game_controller( window , self.parent)
            window.geometry('%dx%d+%d+%d' % (209,670, x*214, 28))
            self.game_list[x] = (window, control)
        
        for game_index in self.game_list:
            if game_index > 2:
                self.hide_game(game_index)
                self.hidden_games[game_index] = self.game_list[game_index][0]
        
        self.parent.focus_force()
        self.parent.mainloop()    
    
    def show_game(self, game_dex):
        """show game function
        separate from calling function
        
        removes game from dict of hidden games
        shows game window (Toplevel) and restarts game controller
        """
        if game_dex not in self.hidden_games:
            print "not hidden"
            return
        self.hidden_games[game_dex] = None
        del self.hidden_games[game_dex]
        
        for key in self.hidden_games:
            print "key: " + str(key)
        window, control = self.game_list[game_dex]
        window.update()
        window.deiconify()
        control.restart()
        
        
    def hide_game(self, game_dex):
        """hide game function
        separate from calling function
        
        add game (window) to dict of hidden games
        hide game window (Toplevel)
        """
        pass
        window = self.game_list[game_dex][0]
        self.hidden_games[game_dex] = window
        window.withdraw()

    
    def switch_callback(self, event):
        """callback function for game switch, show/hide games
        
        TODO: have better solution than one callback for both switch and show/hide
        
        checks if add/remove has been toggled in current game controller
            if so, calls add/remove process function and returns focus to current game
        else
            switches in L->R order
            also prevents switching to hidden games (since games are hidden/shown
                always on the right)
            
        works in conjunction with tetris_base_adapt space_callback
            to highlight active game and darken idle games
        "                                         " minus_, plus_callback
            to check for and show/hide games
        """
        if not self.game_list:
            print "not yet started"
            return
        
        current_window, current_game = self.game_list[self.active_game]
        if current_game.plus:
            print "adding a game"
            current_game.plus = False
            current_game.minus = False
            self.process_add()
            current_window.focus_force()
            return
        elif current_game.minus:
            print "removing a game"
            current_game.plus = False
            current_game.minus = False
            hide_game_dex = self.process_remove()
            if hide_game_dex != self.active_game:
                current_window.focus_force()
                return
            
        self.active_game = (self.active_game + 1) % self.num_games
        while self.active_game in self.hidden_games:    # if the "next" game is hidden...
            self.active_game = (self.active_game + 1) % self.num_games
        
        if self.active_game >= self.num_games:
            print "game out of bounds error"
            self.active_game = 0
        next_window, next_game = self.game_list[self.active_game]
        next_window.lift()
        next_game.board.canvas.config(bg='mint cream')
        next_window.focus_force()
        return 'break'
    
    def process_add(self):
        """processes game adding
        
        checks for next game to be shown
        ensures that games are only added at right ('high' indices)
            and that only 6 games are shown
        """
        pass
        game_dex = 0
        while game_dex not in self.hidden_games:
            game_dex += 1
        if game_dex >= self.num_games:
            print "can't add more"
            return
        self.show_game(game_dex)
        
    def process_remove(self):
        """processes game removal
        
        checks next game to be hidden
        ensures that games are only removed from right ('high' indices)
            and that leftmost game stays visible
        """
        pass
        game_dex = self.num_games - 1
        while game_dex in self.hidden_games:
            game_dex -= 1
        if game_dex <= 0:
            print "can't remove more"
            return
    #    s = 'keys: '                       # debug code
    #    for key in self.hidden_games:
    #        s += str(key) + ' '
    #    print s
        self.hide_game(game_dex)
        return game_dex


if __name__ == "__main__":
    
    print "\nwelcome to Multi-Tetris_adapt!\nto quit, just close the Tk GUI windows or quit Tk\n"
#    print "please enter number of games"               # could possibly be used for changing max number of games
#    num_games = int(raw_input('num games? > '))
#    print "entry disregarded: starts with three."
    
    
    root = tk.Tk()
    
    multi = Tetris_Switcher(root)
    multi.start()