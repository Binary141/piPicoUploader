#!/usr/bin/env python3

#from icecream import ic
import io, os, sys, serial, glob
from serial.tools import list_ports
import signal


def get_port():
    ports = list_ports.comports()
    for port, desc, hwid in sorted(ports):
            if "Board in FS mode" in desc:
                return port.strip()
            return None


devPath = get_port()
#ic(devPath)

if not devPath:
    print('Fatal error, serial port not found.')
    exit(1)

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
