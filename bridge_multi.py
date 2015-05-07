""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 bridge_multi.py
 
 Main control hub and thread for bridge server, combined with Multi-Tetris
    Contains main() function
    Integrates with pupil.py, record.py, multitetris.py
    
 DEPENDENCIES:
    Tkinter     -   Tk bindings for Python (included with Python)
 ---------------------------------- (O)<< ----------------------------------------------
"""

############################################################
# COMMENTS: prob just enough for someone w/ a little coding exp to know what each fcn does
############################################################

import subprocess, os, sys
import threading
from Queue import Queue
import time     # mainly for debugging purposes, giving time for threads to startup

import pupil
import record

import Tkinter as tk
import multitetris as mt


# RESOURCES
#   threading tutorial: http://pymotw.com/2/threading/index.html#module-threading
#   shell escape chars: http://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python
#   Tkinter crash with raw_input: http://stackoverflow.com/questions/15817554/obscure-repeatable-crashes-in-multi-threaded-python-console-application-using-t



def shellformat(string):
    """helper function for formatting shell commands
    """
    return "'" + string.replace("'", "'\\''") + "'"


def start_pupil():
    """thread function to start Pupil Capture
    CHANGE THE PATH BELOW to your local copy of Pupil Capture
    """
    # runs Pupil Capture from source
    path = os.path.abspath("../../pupil/pupil_src/capture/main.py")
    return subprocess.call('python ' + shellformat(path), shell=True)
    
    # if running Pupil Capture using the app, comment the above code and uncomment below:
    '''
    path = os.path.abspath("../pupil_capture_0.4.1_mac.app")
    return subprocess.call('open ' + shellformat(path), shell=True)
    '''

def start_multitetris():
    """thread function to start Pupil Capture
    """
    path = os.path.abspath("multitetris.py")
    return subprocess.call('python ' + shellformat(path), shell=True)


def bridge_main(out_file, num_games):
    """main function 
    starts Pupil Capture, readies and runs listener, remote, and record threads
    Multi-Tetris runs in main thread
    """
    print "*******\nall interaction with the bridge server will occur in the console.\n*******"
    print "loading..."
    starter = threading.Thread(name='starter', target=start_pupil)
    starter.setDaemon(False)
    starter.start()
    
    time.sleep(7)
    
    pupil_data = Queue()            # to store pupil data between listener <-> recorder
    sig_remote_listen = Queue()     # for message passing between remote <-> listener
    sig_listen_record = Queue()     # for message passing between recorder <-> listener
    
    
    cmd = raw_input("enter a char once Pupil Capture has started. > ")
    if cmd:
        print "ready."
        pass
    else:
        print "also ready."
        pass
    
    ear = pupil.Listener(pupil_data, remote_sig=sig_remote_listen, record_sig=sig_listen_record)
    ear.setDaemon(False)
    ear.start()    
    
    mouth = pupil.Remote(sig_remote_listen)
    mouth.setDaemon(False)
    mouth.start() 

    scribe = record.Recorder(out_file, pupil_data, sig_listen_record)
    scribe.setDaemon(False)
    scribe.start()

    print "loading Multi-Tetris..."
    time.sleep(5)
    
    # Tk root must run in main thread, so bridge main handles multi-tetris.
    root = tk.Tk()
    multi = mt.Tetris_Switcher(root, num_games)
    multi.start()


    print "bridge main thread finished"

    # to end program, quit Pupil Capture and Multi-Tetris GUI windows after all threads finish.
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "\nPlease include an output file name!"
        exit()
    if len(sys.argv) < 3:
        print "\nPlease include number of games for Multi-Tetris!"
        exit()

    out_file = sys.argv[1]
    n_games = int(sys.argv[2])
    
    bridge_main(out_file, n_games)
    