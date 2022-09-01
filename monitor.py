#!/usr/bin/env python3

import io, os
import signal

devPath = os.popen("./devFinder.sh | grep MicroPython | awk '{print $1}'").read().strip()

def handler(signum, frame):
    exit(1)
 
signal.signal(signal.SIGINT, handler)
 
count = 0
while True:
    tty = io.TextIOWrapper(
            io.FileIO(
                os.open(
                    devPath,
                    os.O_NOCTTY | os.O_RDWR),
                "r+"))

    for line in iter(tty.readline, None):
        print(line.strip())
