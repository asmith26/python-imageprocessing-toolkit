from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import range
import matplotlib.pyplot as plt
import numpy as np

#import cv2
from skimage.io import imread, imshow, imsave
from scipy.misc import imresize
import os
from random import randint
import logging
#LOG_FILENAME = 'logging_example.out'
#logging.basicConfig(filename=LOG_FILENAME,
logging.basicConfig(level=logging.INFO,
                    )

dir = os.path.dirname(__file__)
GH = os.path.join(dir, "../tests/data/GH.jpg")

class ImageArray(object):

    def __init__(self, img_path=GH, np_path=None,  arr=None, channels=3):
        self.channels = channels
        if img_path != None:
            self.path = img_path
            self.img2arr()
        elif np_path != None:
            self.arr = np.load(np_path)
        elif arr != None:
            self.arr = arr
        else:
            raise InputError("Please initialise class with either argument 'img_path', 'np_path' or 'arr'.")


    def __repr__(self):
        return "self.arr=\n\n{}".format(self.arr)
        

    def img2arr(self):
        if self.channels == 3:   # RGB
            self.arr = imread(self.path, as_grey=False)
        elif self.channels == 1: # grayscale
            self.arr = imread(self.path, as_grey=True)

    def order_ocv2ker(self, keras_order):
        """ Return a given numpy (image) array with Keras dimension ordering.
            default order (cv2)=(height, width, channels)
            order={'th'=Theano, 'tf'=TensorFlow} where:
                'th': (channels, width, height)
                'tf': (width, height, channels)
        """
        print("WARNING: Only convert to Keras format after completing all pre-processing steps.")
        if keras_order == "th":
            self.arr = self.arr.transpose((2,1,0))
            assert(self.arr.shape[0]==1 or self.arr.shape[0]==3)
        elif keras_order == "tf":
            self.arr = self.arr.transpose((1,0,2))
            assert(self.arr.shape[2]==1 or self.arr.shape[2]==3)
        else:
            raise ValueError("keras_dim_ordering='th' or 'tf'.")
    

    def show_img(self,  name='image'):
        if self.channels == 1:
            plt.imshow(self.arr, cmap='Greys_r')
        elif self.channels == 3:
            plt.imshow(self.arr)
        plt.show()

    def save_img(self, filepath='/tmp/ImageArray.jpg'):
        imsave(filepath, self.arr)

    def save_arr(self, filepath='/tmp/ImageArray'): # automatically adds '.npy' extension
        np.save(filepath, self.arr)

    def height(self):
        return self.arr.shape[0]

    def width(self):
        return self.arr.shape[1]

    def resize(self, height, width):
        self.arr = imresize(self.arr, (height, width))

    def crop(self, pixels_width=None, pixels_height=None, percent_width=None, percent_height=None): # ToDo: random_n=None (or number of random number of crops to make)
        """ Returns a crop image specified by pixel starting/ending positions or reduces
            width/height by a specified percentage.

            Input: pixels_width or pixels_height:=tuples, pixels to (start_left, end_right) and (start_top, end_bottom)
                xor percent_width or percent_height:=floats, percentage to reduce width/height by.

            Example:
                
        """
        if percent_width or percent_height:##height, width, channels
            if percent_width:
                logging.debug("Cropping width by percent_width={}".format(percent_width))
                assert(percent_width >=0 and percent_width <= 1)
                width_reduction = (percent * self.width()) // 2
                start_left = width_reduction
                end_right = self.width() - width_reduction
                self.arr = self.arr[:, start_left:end_right, :]

            if percent_height:
                logging.debug("Cropping width by percent_height={}".format(percent_height))
                assert(percent_height >=0 and percent_height <= 1)
                height_reduction = (percent * self.width()) // 2
                start_top = height_reduction
                end_bottom = self.height() - height_reduction
                self.arr = self.arr[start_top:end_bottom, :, :]
                
        elif pixels_width or pixels_height:
            if pixels_width:
                start_left = pixels_width[0]
                end_right = pixels_width[1]
                logging.debug("Cropping width to pixels=[:, {0}:{1}, :]".format(start_left, end_right))
                assert(start_left >= 0 and end_right <= self.width)
                self.arr = self.arr[:, start_left:end_right, :]

            if pixels_height:
                start_top = pixels_height[0]
                end_bottom = pixels_height[1]
                logging.debug("Cropping height to pixels=[{0}:{1}, :, :]".format(start_top, end_bottom))
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
