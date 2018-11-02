"""
https://www.pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/
"""

import cv2
import numpy as np


def calculate_image_colorfulness(image):
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))

    # compute rg = R - G
    rg = np.absolute(R - G)

    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)

    # compute the mean and standard deviation of both `rg` and `yb`
    (rb_mean, rb_std) = (np.mean(rg), np.std(rg))
    (yb_mean, yb_std) = (np.mean(yb), np.std(yb))

    # combine the mean and standard deviations
    std_root = np.sqrt((rb_std ** 2) + (yb_std ** 2))
    mean_root = np.sqrt((rb_mean ** 2) + (yb_mean ** 2))

    # derive the "colorfulness" metric and return it
    return std_root + (0.3 * mean_root)
