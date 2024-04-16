# piPicoUploader

## About
This is just a simple project that allows uploading of a .py file and viewing the output of a Raspberry Pi Pico using [ampy](https://pypi.org/project/adafruit-ampy/). 

## Setup
You may receive an error stating that the device cannot be accessed. In this case, you may need to add your user to the group that is in control of the tty device. On Ubuntu, this is most commonly the `dialout` group, and you can add yourself to that group using the command `sudo usermod -a -G dialout $USER`. On Manjaro the group that was in control of my device was the `uucp` group so my command was `sudo usermod -a -G uucp $USER`. If you would like to make sure you are assigning yourself to the correct group, you can issue the command `ls -l /dev/ | grep <device>` and you can see it there.

After adding yourself to that group you may have to either log out and log back in, or simply reboot to apply the permissions. In my case I had to reboot, but others have stated a log out and log in worked for them. 


## Usage
To use this, simply make the python file executable using `chmod +x uploader.py`, and run `./uploader.py -f <file_name>` in the command line. Then it will take the file and upload it to the device that `devFinder.sh` finds.

Optionally you can use the `-m` flag to monitor the output of the pico, ex. `./uploader.py -m -f <filename>` and it will upload the given file to the Pico and print out the output into the terminal window. You can optionally use the `monitor.py` file to simply just monitor the output without uploading any code, ex `./monitor.py`

The `test.py` file is just to make sure that the uploader is working correctly, and just blinks the onboard led of the pico.

![usage gif](https://github.com/Binary141/piPicoUploader/blob/main/usage.gif)
