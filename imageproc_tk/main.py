#!/usr/bin/env python

import numpy as np
import cv2
import os
dir = os.path.dirname(__file__)
GH = os.path.join(dir, "../test/data/GH.jpg")


class ImageArray(np.ndarray):

    def __init__(self, img_path=GH, channels=3, keras_dim_ordering="th"):
        """ (str, int, str) -> nd.array """ #GET THIS WORKING
        self.path = img_path
        self.channels = channels
        self.img2arr()
        self.keras_dim_ordering = keras_dim_ordering
        # 'th'=Theano, 'tf'=TensorFlow where:
        #       'th': (samples, channels, width, height)
        #       'tf': (samples, width, height, channels)
        self.reshape_keras_dim_ordering()
        
        

    def img2arr(self):
        if self.channels == 3:   # RGB
            self.arr = cv2.imread(self.path)
        elif self.channels == 1: # grayscale
            self.arr = cv2.imread(self.path, 0)

    def reshape_keras_dim_ordering(self):
        """ Return a given numpy (image) array with Keras dimension ordering.
            order={'th'=Theano, 'tf'=TensorFlow} where:
                'th': (channels, width, height)
                'tf': (width, height, channels)
        """
        if self.keras_dim_ordering == "th":
            self.arr = self.arr.transpose((2,1,0))
        elif self.keras_dim_ordering == "tf":
            self.arr = self.arr.transpose((1,0,2))
        else:
            raise ValueError("keras_dim_ordering='th' or 'tf'.")

    def arr2img(self,  name='image'):
        cv2.imshow(name, self.arr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # scale: (0,1], 1=same input size
    # defaults yield no changes
    def resize(self, set_height=0, set_width=0, scale_width=1, scale_height=1):
        resized = cv2.resize(self.arr,
                             dsize=(set_width, set_height),
                             fx=scale_width, fy=scale_height)
        return resized


    def height(self):
        if self.keras_dim_ordering == "th":
            return self.arr.shape[2]
        elif self.keras_dim_ordering == "tf":
            return self.arr.shape[1]

    def width(self):
        if self.keras_dim_ordering == "th":
            return self.arr.shape[1]     
        elif self.keras_dim_ordering == "tf":
            return self.arr.shape[0]
