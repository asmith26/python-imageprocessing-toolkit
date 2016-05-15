#!/usr/bin/env python

from imageproc_tk.common import *
import pytest

GH_arr = img2arr("data/GH.jpg") # h=848, w=640, c=3

def test_img2arr():
    assert GH_arr.shape == (848,640,3)
    assert img2arr("data/GH.jpg", scale_width=0.5).shape == (848,320,3)
    assert img2arr("data/GH.jpg", set_width=5, set_height=5).shape == (5,5,3)

#    with pytest.raises(TypeError):
#        img2arr(...)

def test_height_width_channels():
    height, width, channels = height_width_channels(GH_arr)
    assert height == 848
    assert width == 640
    assert channels == 3
    

def test_keras_dim_ordering():
    assert keras_dim_ordering(GH_arr, order='th').shape == (3,640,848)
    assert keras_dim_ordering(GH_arr, order='tf').shape == (640,848,3)
    with pytest.raises(ValueError):
        keras_dim_ordering(GH_arr, order='something terribly misguided')
