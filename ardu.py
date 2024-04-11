#!/usr/bin/python
#
# python-v4l2capture
#
# This file is an example of how to capture a picture with
# python-v4l2capture.
#
# 2009, 2010 Fredrik Portstrom
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

import select
import v4l2capture #sudo apt-get install libv4l-dev && sudo pip install v4l2capture
import cv2
import numpy as np
import time 
i = 0
image_width = 1920
image_height = 1080

def print_message():
    text = "This demo is used for Arducam ov9281 camera\r\n\
    press 't' to save image\r\n\
    press 'q' to exit demo\r\n"
    print(text)
    
    
if __name__ == "__main__":
    print_message()
    
    video = v4l2capture.Video_device("/dev/video0")
    
    video.create_buffers(2)
    
    video.queue_all_buffers()
    
    video.start()
    select.select((video,), (), ())
    
    while True:
        image_data = video.read_and_queue()
        #image_data = remove_padding(image_data,image_width,image_height,10)
        image_data = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Arudcam OV9281 Preview",image_data)
        key= cv2.waitKey(delay=5)
        if key == ord('t'):
            cv2.imwrite(str(image_width)+"x"+str(image_height)+"_"+str(i)+'.jpg',image_data)
            i+=1
            print("Save image OK.")
        if key == ord('q') or key == 27:
            break
    cv2.destroyAllWindows()
    video.close()
