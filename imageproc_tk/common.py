#!/usr/bin/env python

import numpy as np
import cv2

def arr2img(arr, name='image'):
    cv2.imshow(name, arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# scale: (0,1], 1=same input size
def img2arr(img_path, set_height=0, set_width=0,  scale_width=1, scale_height=1, channels=3):
    if channels == 3:   # RGB
        img = cv2.imread(img_path)
    elif channels == 1: # grayscale
        img = cv2.imread(img_path, 0)
    resized = cv2.resize(img,
                         dsize=(set_width, set_height),
                         fx=scale_width, fy=scale_height)
    return resized
