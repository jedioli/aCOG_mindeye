""" 
 ---------------------------------- (O)<< ----------------------------------------------
 aCOG - Beyond the Mind's Eye
 Copyright (C) 2015  Oliver Hatfield, Sara Fox, Benjamin Sitz, Benjamin Sullivan

 npy_out.py

 ---------------------------------- (O)<< ----------------------------------------------
"""

# RESOURCES
#   https://github.com/pupil-labs/pupil/wiki/Data-format
#   http://stackoverflow.com/questions/6081008/dump-a-numpy-array-into-a-csv-file
#   http://stackoverflow.com/questions/8386675/extracting-specific-columns-in-numpy-array
#   http://stackoverflow.com/questions/1703505/excel-date-to-unix-timestamp
#   http://stackoverflow.com/questions/12223167/adding-header-to-numpy-array


import os, sys
import numpy




if len(sys.argv) < 3:
    print "\nPlease include the path to a NumPy data file, and the output file name, as command line arguments."
    exit()


path = os.path.abspath(sys.argv[1])
pupil_data = numpy.load(path)

#   output_file = "junkyjunk.csv"
output_file = sys.argv[2]

print "data ready"
print "num data points = " + str(pupil_data.shape[0])

if len(pupil_data.shape) == 1:
    print "eye camera timestamps"
    top = 'timestamp'
    numpy.savetxt(output_file, pupil_data, delimiter=",", header=top)
    exit()
    
print "num cols = " + str(pupil_data.shape[1])

select_data = pupil_data[:, [0, 1, 5]]
top_head = 'timestamp, confidence, diameter'

numpy.savetxt(output_file, select_data, delimiter=",", header=top_head)

print "data output to file: " + output_file