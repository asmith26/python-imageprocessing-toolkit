#!/usr/bin/env python

import numpy as np
import cv2
from imageproc_tk.main import ImageArray

class ImagePreprocessing(ImageArray):

    def __init__(self, img_path, channels=3):
#        super(ImagePreprocessing, self).__init__(self)
        ImageArray.__init__(self, img_path, channels)


def crop(arr):
    img = cv2.imread(img)
    crop_img = img[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
