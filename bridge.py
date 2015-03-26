""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 bridge.py

 ---------------------------------- (O)<< ----------------------------------------------
"""

import subprocess, os
#import multiprocessing
import threading
from Queue import Queue
import time     # mainly for debugging purposes

import pupil
import record



# RESOURCES
#   threading tutorial: http://pymotw.com/2/threading/index.html#module-threading
#   shell escape chars: http://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python


# NOTES:
#   I think I'll start out with just threading, and only if I have problems will I go to multiprocessing.
#   I could probably consolidate record into this module, since I could probably output once everything else is done.
#       Also wouldn't have to pass messages to other threads and junk.
#       I could maybe do the same with Pupil Remote? Just put it in a function?





# ---:
#   you know, this might not even be necessary. we might as well just fire up pupil
#       ourselves. we just need to send start/stop signals.
#   FOUND IT! just enclose the file path in quotes!! see resource above.

def shellformat(string):
    return "'" + string.replace("'", "'\\''") + "'"

def start_pupil():
    path = os.path.abspath("../pupil/pupil_src/capture/main.py")
    return subprocess.call('python ' + shellformat(path), shell=True)
    
    '''
    path = os.path.abspath("pupil_capture_0.4.1_mac.app")
    return subprocess.call('open ' + shellformat(path), shell=True)
    '''




if __name__ == '__main__':
    
#    start_pupil()
    
    starter = threading.Thread(name='starter', target=start_pupil)
    starter.setDaemon(False)
    starter.start()
    
    time.sleep(5)
    
    pupil_data = Queue()
    
    
    ear = pupil.Listener(pupil_data)
    ear.setDaemon(False)
    ear.start()
    
    
    scribe = record.Recorder('actual_test.csv', pupil_data)
    scribe.setDaemon(False)
    scribe.start()
    
    time.sleep(5)
    
    ear.stop()
    scribe.ready()
    
    '''
    stuff = Queue()
    stuff.put({'diameter' : 40, 'timestamp' : 2000})
    stuff.put({'diameter' : 50, 'timestamp' : 2001})
    stuff.put({'diameter' : 60, 'timestamp' : 2002})
    stuff.put({'diameter' : 45, 'timestamp' : 2003})
    stuff.put({'diameter' : 50, 'timestamp' : 2004})
    stuff.put({'diameter' : 70, 'timestamp' : 2005})
    
    scribe = record.Recorder('boogaloo.csv', stuff)
    scribe.setDaemon(False)
    scribe.start()
    
    stuff.put({'diameter' : 30, 'timestamp' : 2006})
    stuff.put({'diameter' : 20, 'timestamp' : 2007})
    stuff.put({'diameter' : 80, 'timestamp' : 2008})
    stuff.put({'diameter' : 75, 'timestamp' : 2009})
    
    scribe.ready()
    '''
    
    '''
    mouth = pupil.Remote()
    mouth.setDaemon(False)
    mouth.start()
    '''
    
    
#    ear.daemon = False
#    mouth.daemon = False
    
#    ear.start()
#    mouth.start()