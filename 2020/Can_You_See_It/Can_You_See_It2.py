import cv2
import time
import os
import sys
import numpy as np


def get_divisors(n):
    for i in range(8, int(n / 2) + 1):
        if n % i == 0:
            yield i
    yield n

for i in sys.argv[1:]:
    bindata = np.fromfile('data2', dtype='uint8')[int(i):]

    n = int(len(bindata))
    dims = [(c, int(n/c)) for c in get_divisors(n)]
    #dims = [(int(n/12), 12)]
    for d in dims:
        nd = bindata.reshape(d)
        cv2.imwrite("image_%dx%d.bmp" % (d), nd)
