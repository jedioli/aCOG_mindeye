""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 record.py

    Used to record pupil size data streamed from Pupil Capture to the bridge server
    Contains Recorder class
    Integrates with bridge.py, pupil.py
    
 DEPENDENCIES:
    none
 ---------------------------------- (O)<< ----------------------------------------------
"""


from threading import Thread
import Queue                    # for passing messages between threads
import csv


# RESOURCES:
#   https://docs.python.org/2/library/queue.html
#   http://pymotw.com/2/threading/index.html#module-threading
#   http://pymotw.com/2/Queue/index.html#module-Queue
#   https://docs.python.org/2/library/csv.html, particularly the DictWriter object
#   http://stackoverflow.com/questions/13254241/removing-key-values-pairs-from-a-list-of-dictionaries


# NOTE:
#   Pupil Server by default streams ['timestamp', 'diameter', 'confidence', 'norm_pos', 'id']
#       'norm_pos' and 'id' are not needed.
#   Earlier versions of this project modified the Pupil Server code in source,
#       but a more robust version is given here.


class Recorder(Thread):
    """recorder thread
    awaits signal from listener thread that data collection complete
    records data to .csv or .txt
        
    socket and port configured for Pupil Remote defaults
    """
    def __init__(self, fn, queue, signal):
        super(Recorder, self).__init__()
        self.filename = fn
        self.pupil_data = queue     # thread-safe Queue for storing pupil data
        self.sig_listen = signal    # Queue for signaling when to start recording
    #    print 'recorder inited'
        
    def run(self):
        """thread run function
        awaits signal from pupil.Listener thread
        outputs data in message Queue to file
        """  
        while self.sig_listen.empty():
            pass
        signal = self.sig_listen.get()
        print "ready to output to file"
        status = self.tofile()
        if status:
            print "data is output"
        else:
            print "record failure"
        return
        
    def tofile(self):
        """file output function
        can output to .txt or .csv
        
        to include other data fields, modify 'header' and 
            the dict comprehension for 'datum' below
        """  
        if self.filename[-3:] == 'txt':
            with open(self.filename, 'w') as f:
                while not self.pupil_data.empty():
                    datum = self.pupil_data.get()
                    f.write(str(datum) + '\n')
            pass
            return True
        
        # this version assumes each datum is a dict object
        elif self.filename[-3:] == 'csv':
            with open(self.filename, 'w') as f:
                if self.pupil_data.empty():
                    print "no data to output!"
                    return False
                    
                header = ['timestamp', 'diameter', 'confidence']
                    # other header fields include: ['timestamp', 'diameter', 'major', 'ellipse', 'norm_pos', 'confidence', 'id', 'roi_center']
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                while not self.pupil_data.empty():
                    temp_datum = self.pupil_data.get()
                    # remove unnecessary key:value pairs from datum
                    datum = {key: value for key, value in temp_datum.iteritems() if 
                           (key == 'timestamp' or
                            key == 'diameter' or
                            key == 'confidence')}
                    writer.writerow(datum)  
            pass
            return True
        else:
            print "file type not recognized"
            return False