""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 pupil.py

    Used to monitor data stream, send commands to Pupil Capture via ZeroMQ-TCP
    Contains Listener and Remote classes
    Integrates with bridge.py, record.py
    Network connections (localhost) specifically tuned to Pupil Capture Server module
    
 DEPENDENCIES:
    zmq     -   ZeroMQ network library (Python bindings)
 ---------------------------------- (O)<< ----------------------------------------------
"""


import zmq
from threading import Thread
import Queue    # for thread-safe message passing, to workload.py and to record.py

import sys

# RESOURCES
#   http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies
#   https://docs.python.org/2/library/multiprocessing.html
#   http://stackoverflow.com/questions/509211/explain-pythons-slice-notation




class Listener(Thread):
    """Pupil Server listener thread
    receives messages from Pupil Server streamed over TCP with ZeroMQ

    socket and port configured for Pupil Server defaults
    """
    def __init__(self, queue, remote_sig, record_sig):
        super(Listener, self).__init__()
        data_port = "5000"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:" + data_port)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self.pupil_data = queue
        self.sig_remote = remote_sig
        self.sig_record = record_sig
        self.put_counter = 0
    
    
    def run(self):
        """thread run function
        waits to receive signal from remote, then listens to stream
        
        can await multiple signals in the same session (toggles)
        """
        while self.sig_remote.empty():    # wait for starting signal from remote
            pass
        signal = self.sig_remote.get()
        
        recording = False
        
        while signal[1] != 'finish':
            if signal[1] == 'toggle' and not recording:
                print "starting to listen"
                recording = True
                while self.sig_remote.empty():
                    self.listen()
            elif signal[1] == 'toggle' and recording:
                print "stopping to listen"
                recording = False
                while self.sig_remote.empty():
                    pass
            signal = self.sig_remote.get()
                
        print "done listening: " + str(self.put_counter) + " events"
        self.sig_record.put(("record","start"))
        return
    
    
    def listen(self):
        """receives streamed message, formats data as a dict, and puts in data Queue
        """
        data_msg = self.socket.recv()

        items = data_msg.split("\n") 
        msg_type = items.pop(0)
        data_dict = dict([i.split(':') for i in items[:-1] ])
    
        if msg_type == 'Pupil':
        #    print data_msg         # uncomment this to stream data to the console
            self.pupil_data.put(data_dict)
            self.put_counter += 1
        else:
            # these are all "Gaze" events, but only ever lists timestamp and confidence.
            #   unused in aCOG_mindeye.
            pass
        pass




class Remote(Thread):
    """Pupil Remote commander thread
    sends command messages to Pupil Remote over TCP with ZeroMQ
    allows for external control of recording (start and stop)
        other functions (calibration, resetting timebase) left out
        
    socket and port configured for Pupil Remote defaults
    """
    def __init__(self, signal):
        super(Remote, self).__init__()
        remote_port = '50020'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)      # this protocol requires send/receive pairs
        self.socket.connect("tcp://localhost:" + remote_port)
        self.sig_listen = signal    # signal to listener thread
        self.toggle_count = 0
    
    def run(self):
        """thread run function
        takes input from command line and sends to Pupil Remote
        continues until 'Q' or unexpected input
        """
        while True:
            try:
                print "Please input a remote command to send..."
                print "\tEnter 'R' to toggle recording, or 'Q' to quit."
            #    cmd = raw_input("cmd? > ")             # causes crashes in Tk
                cmd = sys.stdin.readline()
            #    print "repr: " + repr(cmd)
            except EOFError:
                print "Thank you! Terminating..."
                self.sig_listen.put(('listen','finish'))
                break
            if cmd[0] != 'R':   # need to get the first letter with stdin, since captures \n
                print "Thank you! Terminating..."
                self.sig_listen.put(('listen','finish'))
                break
            cmd += '  '             # accounts for bug in pupil_remote.py
            self.notify(cmd)   
        return
    
    def notify(self, cmd):
        """takes command from run() and sends to Pupil Remote
        waits for a confirmation message (required by connection scheme)
        """
        result = self.socket.send(cmd)
        if cmd[0] == 'R':
            self.sig_listen.put(('listen','toggle'))
            self.toggle_count += 1
        if result is None:
            print "command sent!"
        else:
            print "command not sent"
        try:
            print "waiting confirmation"
            confirm = self.socket.recv()
            print confirm
        except zmq.ZMQError:
            confirm = None
            print "zeroMQ error"

