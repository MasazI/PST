#encoding: utf-8
import math
import cv2

import skimage
from skimage import data
from skimage import io
from skimage import transform
from skimage.color import rgb2gray

import numpy as np

class PST:
    def __init__(self):
        self.LPF = 0.21
        self.Phase_strength = 0.48
        self.Warp_strength = 12.14
        self.Thresh_min = -1
        self.Thresh_max = 0.0019
        self.Morph_flag = 1

    def transform(self, image_path):
        image_org = io.imread(image_path)
        #print image_org.shape
        image = rgb2gray(image_org)

        # define two dimentional cartesian vectors, X ans Y
        height = len(image)
        width = len(image[0])
        L = 0.5
        x = np.linspace(-L, L, width)
        y = np.linspace(-L, L, height)
        [X, Y] = np.meshgrid(x, y)

        # convert cartesian X and Y vectors to polar vectors (THETA, RHO) 極座標に変換
        [THETA, RHO] = self.cart2pol(X, Y)

        # define two dimentional cartesian frequency vectors, FX and FY
        X_step = x[1] - x[0]
        fx = np.linspace(-0.5/X_step, 0.5/X_step, len(x))
        #fx_step = fx[1] - fx[0]
        Y_step = y[1] - y[0]
        fy = np.linspace(-0.5/Y_step, 0.5/Y_step, len(y))
        #fy_step = fy[2] - fy[1]

        [FX, FY] = np.meshgrid(fx, fy)

        # convert cartesian FX and FY vectors to polar vectors (FTHETA, FRHO) 極座標に変換
        [FTHETA, FRHO] = self.cart2pol(FX, FY)

        # low pass filter the original image to reduce noise
        image_f = np.fft.fft2(image)
        sigma = (self.LPF)**2/math.log(2)

        image_fftshift = np.fft.fftshift(np.exp(-(RHO/np.sqrt(sigma))**2))
        image_f = image_f * image_fftshift
        image_filtered = (np.fft.ifft2(image_f)).real

        PST_Kernel = (RHO*self.Warp_strength * np.arctan(RHO*self.Warp_strength) - 0.5 * np.log(1 + (RHO * self.Warp_strength)**2))
        PST_Kernel = PST_Kernel / np.max(PST_Kernel) * self.Phase_strength

        temp = np.fft.fft2(image_filtered) * np.fft.fftshift(np.exp(-1j * PST_Kernel))
        image_filtered_PST = np.fft.ifft2(temp)

        PHI_features = np.angle(image_filtered_PST)

        if self.Morph_flag == 0:
            out = PHI_features
        else:
            features = np.zeros(PHI_features.shape)
            print features



    def cart2pol(self, x, y):
        return np.sqrt(x*x + y*y), np.arctan2(x, y)

if __name__ == '__main__':
    image_path = 'cat.jpg'
    
    pst = PST()
    pst.transform(image_path)
