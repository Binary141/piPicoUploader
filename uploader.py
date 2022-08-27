#!/usr/bin/python3
import sys
import os
from pathlib import Path
import subprocess

#Use the script to find the micropython device, and then remove any whitespace to just isolate the string
devPath = os.popen("./devFinder.sh | grep MicroPython | awk '{print $1}'").read().strip()

#Print the path out each time to make sure that it does grab the correct path. Could use something like Thonny to make sure it is right
print("Device path: ", devPath)

try:
    #Check if the '-f' flag was used to specify a file
    try:
        file = sys.argv[sys.argv.index('-f')+1]
    except:
        sys.exit("You need to specify a file")

    #Check if the file exists, if not then quit the program
    if os.path.isfile(file):
        pass
    else:
        raise Exception("There was an error. Maybe the file doesn't exist")
except Exception as e:
    sys.exit(e)

#This uses ampy to upload the code. Install using pip
cmd = 'ampy --port %s run -n %s'% (devPath, file)

stream = os.popen(cmd) #Execute the command in the command line

stream.close() #Close the stream to be on the safe side
