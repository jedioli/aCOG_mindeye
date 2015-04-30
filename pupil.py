""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 pupil.py

 ---------------------------------- (O)<< ----------------------------------------------
"""


import zmq
from threading import Thread
import Queue    # for thread-safe message sending, to workload and to record.

import sys

# RESOURCES
#   http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies
#   https://docs.python.org/2/library/multiprocessing.html


# NOTES:
#   I think for now I'm just going to use threading, and only move to multiprocessing if I run into trouble.


# QUESTIONS
#   should I derive Thread/Process? or just make functions that threads would target?


class Listener(Thread):
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
#        self.ready = True
        self.put_counter = 0
    
#    def begin(self):
#        self.ready = True        
#    def stop(self):
#        self.ready = False
    
    def run(self):
        '''
    #    signal = (" ", " ")
        while self.sig_remote.empty():    # wait for starting signal from remote
            pass
    #    signal = self.pupil_signal.get()             # clear signal
    #    while signal[0] is not "listen":
    #        self.pupil_signal.put(signal)
    #        signal = self.pupil_signal.get()
    #    signal = (" ", " ")
        signal = self.sig_remote.get()
        print "starting to listen"
    #    while self.ready:
        while self.sig_remote.empty():
            self.listen()
    #    self.pupil_signal.get()
    #    signal = self.pupil_signal.get()
    #    while signal[0] is not "listen":
    #        self.pupil_signal.put(signal)
    #        signal = self.pupil_signal.get()
        '''
    
        while self.sig_remote.empty():    # wait for starting signal from remote
            pass
        signal = self.sig_remote.get()
        
        recording = False
    #    print "---------- SIGNAL: " + str(signal)
        
        while signal[1] != 'finish':                    # 'is' IS IDENTITY TESTING! NOT equality testing!
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
        data_msg = self.socket.recv()

        items = data_msg.split("\n") 
        msg_type = items.pop(0)
        data_dict = dict([i.split(':') for i in items[:-1] ])
    
        if msg_type == 'Pupil':
            print data_msg
            self.pupil_data.put(data_dict)
            self.put_counter += 1
        else:
            # process non gaze position events from plugins here\
            # These are all "Gaze" events, but only ever lists timestamp and confidence. Not sure what it's for.
            pass
        
        """
        while self.put_counter < 50:        # collecting 50 frames for testing
            data_msg = self.socket.recv()

            items = data_msg.split("\n") 
            msg_type = items.pop(0)
            data_dict = dict([i.split(':') for i in items[:-1] ])
    
            if msg_type == 'Pupil':
                self.pupil_data.put(data_dict)
                self.put_counter += 1
                
                '''
                print "raw msg:\n", data_msg
                try:
                    s = ""
                    for key in data_dict:
                        s += str(key) + " "
    
                print "keys are: " + s
                #they are: "norm_pos confidence id timestamp diameter"
                print "norm_gaze: ", items['norm_gaze']

                except KeyError:
                    pass
                '''
            else:
                # process non gaze position events from plugins here\
                # These are all "Gaze" events, but only ever lists timestamp and confidence. Not sure what it's for.
                '''
                print "not Pupil data: " + str(msg_type)
                list = []
                for key in data_dict:
                    list.append(key)
                print list
                '''
                pass
        """
        pass




class Remote(Thread):
    def __init__(self, signal):
        super(Remote, self).__init__()
        remote_port = '50020'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:" + remote_port)
        self.sig_listen = signal
        self.toggle_count = 0
    
    def run(self):
#        while self.toggle_count < 2:
        while True:
            try:
                print "Please input a remote command to send..."
            #    cmd = raw_input("cmd? > ")             # causes crashes in Tk
                cmd = sys.stdin.readline()
                print "command is " + cmd
                print str(type(cmd))
            except EOFError:
                print "Thank you! Terminating..."
                self.sig_listen.put(('listen','finish'))
                break
            if cmd[0] != 'R':   # need to get the first letter with stdin, since captures \n
                print "Thank you! Terminating..."
                self.sig_listen.put(('listen','finish'))
                break
            self.notify(cmd[0])
        return
    
    def notify(self, cmd):
    #    while True:
            '''
            try:
                print "Please input a remote command to send."
                cmd = raw_input("cmd? > ")
            #    print cmd
            except EOFError:
                print
                print "Thank you! Terminating..."
                print
                return
            # relay to pupil remote.
            '''
            result = self.socket.send(cmd)
            if cmd == 'R':
                self.sig_listen.put(('listen','toggle'))
                self.toggle_count += 1
            if result is None:
                print "great!"
            else:
                print "broke"
            try:
                print "waiting confirmation"
                confirm = self.socket.recv()
                print confirm
            except zmq.ZMQError:
                confirm = None
                print "erk"

