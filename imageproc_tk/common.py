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


def height_width_channels(arr):
    a = arr.shape
    return a[0], a[1], a[2]


def keras_dim_ordering(arr, order='th'):
    """ Return a given numpy (image) array with Keras dimension ordering.
        order={'th'=Theano, 'tf'=TensorFlow} where:
            'th': (samples, channels, width, height)
            'tf': (samples, width, height, channels)
    """
    if order == 'th':
        return arr.swapaxes(0,2)
    elif order == 'tf':
    return arr.swapaxes(0,1)
    else:
        raise ValueError("Dim ordering must be order='th' or 'tf'.")
    
    
