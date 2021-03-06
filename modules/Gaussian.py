# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *

BLUR_KERNEL = np.array([])


def apply(img):
    """
    Apply Gaussian blur
    :param img: input image 
    """

    # cv2 thresh -- https://goo.gl/OHjx6d

    # get the kernel
    kernel = blur_kernel()

    # apply 2D Gaussian filter -- https://goo.gl/jfuzjO
    gauss = cv2.filter2D(img, cv2.CV_64F, kernel)

    return util.normalize(gauss)
# end function


def blur_kernel():
    """
    Build 2D Gaussian kernel 
    """

    global BLUR_KERNEL

    # check if it has already been calculated
    if BLUR_KERNEL.shape == cfg.BLUR_SIZE:
        return BLUR_KERNEL
    # end if

    # formula -- https://goo.gl/3AmmaE

    A = cfg.BLUR_CO
    m, n = cfg.BLUR_SIZE
    sx, sy = cfg.BLUR_SIGMA

    x0 = m / 2
    y0 = n / 2

    X = np.arange(m)
    Y = np.arange(n)

    X = np.square((X - x0) / sx)
    Y = np.square((Y - y0) / sy)

    Y, X = np.meshgrid(Y, X)
    BLUR_KERNEL = A * np.exp(-(X + Y) / 2)

    return BLUR_KERNEL
# end function


def run(prev, cur):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    """
    runtime = []
    util.log("Stage", cur, "Gaussian blur")
    for read in util.get_images(prev):
        # open image
        file = util.stage_image(read, prev)
        img = cv2.imread(file, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(apply, img)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
