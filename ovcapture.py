import numpy as np
import cv2
import v4l2capture
import select
import time
import random
import keyboard

video = v4l2capture.Video_device("/dev/video0")
    
video.create_buffers(2)

video.queue_all_buffers()

video.start()
select.select((video,), (), ())

while True:
    image_data = video.read_and_queue()
    
    key = cv2.waitKey(5)
    
    if key == ord('q'):
        print("quitting ...")
        video.close()
        break
    
    if key == ord('p'):        
        frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        cv2.imwrite("capture.jpg", frame)
        
        print("photo saved")
        
