# piPicoUploader

## About
This is just a simple project that allows uploading of a .py file to a pi pico using [ampy](https://pypi.org/project/adafruit-ampy/). This doesn't include any way of reading the output of the pico, but that can be done using screen. Example usage that can see the output of the pico while it is running would be `screen /dev/<device_path>`, so if my device was located at `/dev/ttyACM0` then my command would be `screen /dev/ttyACM0`

## Usage
To use this, simply make the python file executable, and run `./uploader.py -f <file_name>` in the command line. Then it will take the file and upload it to the device that `devFinder.sh` finds.
