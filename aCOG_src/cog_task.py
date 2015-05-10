""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 Distributed under the terms of the Apache v.2 License.
 .............................................

 cog_task.py

 ---------------------------------- (O)<< ----------------------------------------------
"""


# NOTES:
#   March 2015:
#       this module will contain resources for monitoring and modifying Multi-Tetris.
#
#   May 2015:
#       due to the fact that Tk needs to run in the main thread, this may or may not be 
#           needed. I can potentially see an interface via zeroMQ, but direct function
#           calls might not work. this would definitely require a separate thread.
#
#       actually, this is DEFINITELY needed if I want to modify Multi-Tetris externally.
#           Tk hogs the entire bridge main thread, so only another thread (that holds
#           a reference to the Tetris_Switcher!!) could mess with it.
#
#   for now, this module left intentionally empty.