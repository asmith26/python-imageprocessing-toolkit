#!/usr/bin/env python

import numpy as np
import cv2
import os
from random import randint
dir = os.path.dirname(__file__)
GH = os.path.join(dir, "../test/data/GH.jpg")


class ImageArray(object):

    def __init__(self, img_path, channels=3, keras_dim_ordering="th"):
        self.path = img_path
        self.channels = channels
        self.img2arr()
        self.keras_dim_ordering = keras_dim_ordering
        # 'th'=Theano, 'tf'=TensorFlow where:
        #       'th': (samples, channels, width, height)
        #       'tf': (samples, width, height, channels)
        #self.reshape_keras_dim_ordering()  # DO THIS AT THE END OF ALL PREPROCESSING

    def __repr__(self):
        return "self.arr=\n\n{}".format(self.arr)
        

    def img2arr(self):
        if self.channels == 3:   # RGB
            self.arr = cv2.imread(self.path)
        elif self.channels == 1: # grayscale
            self.arr = cv2.imread(self.path, 0)

    def reshape_keras_dim_ordering(self):
        """ Return a given numpy (image) array with Keras dimension ordering.
            default order (cv2)=(height, width, channels)
            order={'th'=Theano, 'tf'=TensorFlow} where:
                'th': (channels, width, height)
                'tf': (width, height, channels)
        """
        if self.keras_dim_ordering == "th":
            self.arr = self.arr.transpose((2,1,0))
            assert(self.arr.shape[0]==1 or self.arr.shape[0]==3)
        elif self.keras_dim_ordering == "tf":
            self.arr = self.arr.transpose((1,0,2))
            assert(self.arr.shape[2]==1 or self.arr.shape[2]==3)
        else:
            raise ValueError("keras_dim_ordering='th' or 'tf'.")

    def arr2img(self,  name='image'):
        cv2.imshow(name, self.arr)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

    def height(self):
        return self.arr.shape[0]

    def width(self):
        return self.arr.shape[1]

    def resize(self, set_height=0, set_width=0, scale_width=1, scale_height=1):
        # scale: (0,1], 1=same input size
        # defaults yield no changes
        self.arr = cv2.resize(self.arr,
                             dsize=(set_width, set_height),
                             fx=scale_width, fy=scale_height)

    def crop(self, pixels_width=None, pixels_height=None, percent_width=None, percent_height=None): # ToDo: random_n=None (or number of random number of crops to make)
        """ Returns a crop image specified by pixel starting/ending positions or reduces
            width/height by a specified percentage.

            Input: pixels_width or pixels_height:=tuples, pixels to (start_left, end_right) and (start_top, end_bottom)
                xor percent_width or percent_height:=floats, percentage to reduce width/height by.

            Example:
                
        """
        if percent_width or percent_height:##height, width, channels
            if percent_width:
                print "Cropping width by percent_width={}".format(percent_width)
                assert(percent_width >=0 and percent_width <= 1)
                width_reduction = (percent * self.width()) // 2
                start_left = width_reduction
                end_right = self.width() - width_reduction
                self.arr = self.arr[:, start_left:end_right, :]

            if percent_height:
                print "Cropping width by percent_height={}".format(percent_height)
                assert(percent_height >=0 and percent_height <= 1)
                height_reduction = (percent * self.width()) // 2
                start_top = height_reduction
                end_bottom = self.height() - height_reduction
                self.arr = self.arr[start_top:end_bottom, :, :]
                
        elif pixels_width or pixels_height:
            if pixels_width:
                start_left = pixels_width[0]
                end_right = pixels_width[1]
                print "Cropping width to pixels=[:, {0}:{1}, :]".format(start_left, end_right)
                assert(start_left >= 0 and end_right <= self.width)
                self.arr = self.arr[:, start_left:end_right, :]

            if pixels_height:
                start_top = pixels_height[0]
                end_bottom = pixels_height[1]
                print "Cropping height to pixels=[{0}:{1}, :, :]".format(start_top, end_bottom)
                assert(start_top >= 0 and end_bottom <= self.height)
                self.arr = self.arr[start_top:end_bottom, :, :]
        else:
            raise ValueError("\n\nNo Inputs specified:\nUse inputs: pixels_width or pixels_height:=tuples, pixels to (start_left, end_right) and (start_top, end_bottom)\nxor percent_width or percent_height:=floats, percentage to reduce width/height by")


    def random_black_lines(self, n_lines=100):
        for i in xrange(n_lines):
            random_horizontal = randint(0, self.width())
            random_vertical = randint(0, self.height())
            self.arr[:,random_horizontal,:] = 0 # horizontal black line
            self.arr[random_vertical,:,:] = 0 # vertical black line
