#!/usr/bin/python3
import shutil
import sys
import os, io
import serial, glob
from serial.tools import list_ports
from pathlib import Path
import re
import ast, traceback

def checkListDevices():
    try:
        flag_index = sys.argv[sys.argv.index('-l')]
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print(port, desc, hwid)
        sys.exit(0)

    except Exception as e:
        pass

def usage():
        print("Basic Usage:\n")
        print("-f <file_path>: Specify a file to be ran")
        print("-u: Indicates that the file should be uploaded to the Pico and will be ran upon startup")
        print("-m: Monitor the output of the pico")
        print("-d <device_path>: Specify the device path to interact with (useful when you have multiple picos plugged into a single computer\n")
        sys.exit(0)

def checkHelpFlag():
    try:

        if len(sys.argv) == 1:
            # if no arguments are passed in, print the usage and quit the program
            usage()

        flag_index = sys.argv[sys.argv.index('-h')]
        usage()

    except Exception as e:
        pass


def monitor(devPath):
    print("To quit, just do Control+c")
    print("Console Output: \n")
    while True:
        tty = io.TextIOWrapper(
                io.FileIO(
                    os.open(
                        devPath,
                        os.O_NOCTTY | os.O_RDWR),
                    "r+"))

        for line in iter(tty.readline, None):
            print(line.strip())
#==================== Check to see if there are any syntax errors =========
def checkSyntax(filePath):
    with open(filePath) as f:
        source = f.read()
    valid = True
    try:
        ast.parse(source)
    except SyntaxError:
        valid = False
        traceback.print_exc()  # Remove to silence any errros
        sys.exit(0)

#============ Get the port location of the pico =================
def get_port():
    try:
        ports = list_ports.comports()
        #print("ports: ", ports)
        for port, desc, hwid in sorted(ports):
            productID = re.search('PID.*[0-9]$', hwid)
            if productID != None:
                try:
                    productID = productID.group(0).split(' ')[0].split('=')[1].split(":")[0].lower()
                    print("PID: ", productID)
                    if (productID == '2e8a'):
                        print("PORT: ", port.strip())
                        return port.strip()
                except Exception as e:
                    pass

    except Exception as e:
        pass

#================== Check for the -d flag to specify device ===============
def checkDeviceFlag():
    devPath = ""
    try:
        devPath = sys.argv[sys.argv.index('-d')+1]

    except Exception as e:
        devPath = get_port()
        if not devPath:
            print('Fatal error, serial port not found.')
            exit(1)
        print(f'Found device serial port at: {devPath}\n')
    return devPath

#================ Check for the -f flag to specify a file to upload ==========
def checkFileFlag():
    try:
        #Check if the '-f' flag was used to specify a file
        file = sys.argv[sys.argv.index('-f')+1]

        if os.path.isfile(file):
            #Check if the file exists, if not then quit the program
            return file

        # if the return doesn't run above, then just raise an exception just in case
        raise Exception("There was an error. Maybe the file doesn't exist?")
    except Exception as e:
        sys.exit(e)


#============ Check for the -u flag to be able to upload the file to the pico ========
def checkUploadFlag(devPath, file):
    uFlag = 0
    try:
        sys.argv.index('-u')
        filePath = sys.argv[sys.argv.index('-f')+1]
        txt = re.search("main.py", filePath)
        if txt == None:
            cmd = 'ampy --port %s put %s /main.py'% (devPath, filePath)
        uFlag = 1
        print("CMD: ", cmd)

        # set the desired file to be uploaded to that of the new path with
        # main.py
    except Exception as e:
        #This uses ampy to upload the code. Install using pip
        cmd = 'ampy --port %s run -n %s'% (devPath, file)
    return uFlag, cmd


def main():
    checkHelpFlag()
    checkListDevices()
    devPath = checkDeviceFlag()
    file = checkFileFlag()
    checkSyntax(file)
    uFlag, cmd = checkUploadFlag(devPath, file)

    #===== Execute the actual command(s) using the command line
    stream = os.popen(cmd)
    stream.close()

    #========== Check for the uFlag ===========
    #If it is present, we probably don't want to monitor the output of the pico

    if uFlag == 0:
        try:

            flag_index = sys.argv[sys.argv.index('-m')+1]
            monitor(devPath)
            #import monitor.py

        except Exception as e:
            #print("An error occured while trying to monitor the output :(")
            sys.exit(0)
    else:
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
