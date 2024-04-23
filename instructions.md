# For OV5640 USB

1. `sudo apt install v4l-utils`
2. `sudo apt-get install libv4l-dev && sudo pip install v4l2capture`
3. `v4l2capture` installation via pip will get aborted. Hence, install `v4l2capture` via this link [GitHub V4L2 Python Build](https://github.com/atareao/python3-v4l2capture/tree/master)
4. Now, check if OV5640 formats are listed from the following command `v4l2-ctl --device /dev/video0 --list-formats-ext`
5. If all goes well, run ovcapture.py
