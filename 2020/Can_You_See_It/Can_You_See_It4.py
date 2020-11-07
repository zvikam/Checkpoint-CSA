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

if True:
    img = cv2.imread('image.bmp')

    n = img.shape[0] * img.shape[1]
    print(n)
    dims = [(c, int(n/c), 3) for c in get_divisors(n)]
    for d in dims:
        print(d)
        nd = img.reshape(d)
        cv2.imwrite("image_%dx%dx%d.bmp" % (d), nd)
