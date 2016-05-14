#!/usr/bin/env python

from SimpleCV import Camera

cam = Camera()

def start_watching():
    while True:
        # Get Image from camera
        img = cam.getImage()
        # Make image black and white
#       img = img.binarize()
        # Draw the text "Hello World" on image
#       img.drawText("Hello World!")
        # Show the image
        img.show()
