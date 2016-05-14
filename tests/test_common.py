#!/usr/bin/env python

from imageproc_tk.common import img2arr
import pytest

def test_img2arr():
    assert img2arr("data/GH.jpg").shape == (848,640,3)
    assert img2arr("data/GH.jpg", scale_width=0.5).shape == (848,320,3)
    assert img2arr("data/GH.jpg", set_width=5, set_height=5).shape == (5,5,3)

#    with pytest.raises(TypeError):
#        img2arr(...)
