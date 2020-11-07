import cv2
import time
import os
import numpy as np


cap = cv2.VideoCapture('Can_You_See_It.mp4')
video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(video_length)

success = True
data = np.ndarray((video_length,3), dtype=np.uint8)
i = 0
if True:
    while success:
        success,image = cap.read()
        if success:
            if np.all(image == image[0]) and image[0][0][0] != 95:
                v = image[0][0]
                data[i]=v
                i += 1
                print(i, video_length, end='\r')

print(data.shape)
d = (0,0)
cv2.imwrite("image.bmp", data)
