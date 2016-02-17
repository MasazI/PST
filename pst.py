#encoding: utf-8
import math
import cv2

import skimage
from skimage import data
from skimage import io
from skimage import transform
from skimage import color

import numpy as np

class PST:
    def __init__(self):
        pass

    def transform(self, image_path):
        image = io.imread(image_path)
        
        # define two dimentional cartesian vectors, X ans Y
        height = len(image)
        width = len(image[0])
        L=0.5
        x = np.linspace(-L,L,height)
        y = np.linspace(-L,L,width)
        [X, Y] = np.meshgrid(x, y)

        print X
        print Y

if __name__ == '__main__':
    image_path = 'cat.jpg'
    
    pst = PST()
    pst.transform(image_path)
