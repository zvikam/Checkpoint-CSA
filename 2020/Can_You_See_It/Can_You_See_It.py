import cv2
import time
import os
import numpy as np


convert = {
    250: '0',
    95: '',
    0: '1'
    #[250, 253, 251]: '1',
    #[95, 98, 96]: '',
    #[0, 0, 0]: '0'
}


cap = cv2.VideoCapture('Can_You_See_It.mp4')
video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
#print ("Number of frames: ", video_length)

success = True
bindata = bytes()
data = ''
i = 0
with open('data3', 'wb') as fout:
    while success:
        success,image = cap.read()
        if success:
            if np.all(image == image[0]):
                v = convert[image[0][0][0]]
                #print(v, end='')
                data += v
            else:
                cv2.imwrite("frame%d.bmp" % i, image)
            i += 1
            if i % 16 == 0:
                #print(chr(int(data, 2)), end='')
                #bindata += bytes([int(data, 2)])
                fout.write(bytes([int(data, 2)]))
                data = ''

#print(bindata, end='')
