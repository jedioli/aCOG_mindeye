""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 record.py

 ---------------------------------- (O)<< ----------------------------------------------
"""


from threading import Thread
import Queue
import csv


# RESOURCES:
#   https://docs.python.org/2/library/queue.html
#   http://pymotw.com/2/threading/index.html#module-threading
#   http://pymotw.com/2/Queue/index.html#module-Queue
#   https://docs.python.org/2/library/csv.html, particularly the DictWriter object

# NOTES:
#   this Queue class seems really useful. maybe try using join() and task_done()?


class Recorder(Thread):
    def __init__(self, fn, queue):
        super(Recorder, self).__init__()
        self.filename = fn
        self.pupil_data = queue   # this is a thread-safe Queue, it just holds onto the reference
        self.begin = False
        print 'inited'
        
    def run(self):
        while not self.begin:
        #    print 'waiting'
            pass
        else:
            print 'ready'
            self.tofile()
        #    print 'data has ' + str(self.data.qsize()) + ' items in it'     # use qsize() for approx size of queue
            print "data output"
            return
    
    def ready(self):        # set when all data has been collected
        self.begin = True
        
    def tofile(self):
        if self.filename[-3:] == 'txt':
            with open(self.filename, 'w') as f:
                while not self.pupil_data.empty():
                    datum = self.pupil_data.get()
                    f.write(str(datum) + '\n')
            pass
        
        
        # this version assumes each datum is a dict
        if self.filename[-3:] == 'csv':
            with open(self.filename, 'w') as f:
                if self.pupil_data.empty():
                    print "no data to output!"
                    return
            #    datum = self.pupil_data.get()
            #    header = []
            #    header = ['timestamp', 'diameter', 'major', 'ellipse', 'norm_pos', 'confidence', 'id', 'roi_center']
                header = ['timestamp', 'diameter', 'confidence']
                '''
                for key in datum:
                    header.append(key)
                while not self.pupil_data.empty():
                    datum = self.pupil_data.get()
                    for key in datum:
                        if key not in header:
                            header.append(key)
                print "list of column headers:"
                print header
                '''
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
            #    writer.writerow(datum)
                while not self.pupil_data.empty():
                    datum = self.pupil_data.get()
                    writer.writerow(datum)
                
            pass