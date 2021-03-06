# -*- coding: utf-8 -*-

import cv2
import numpy as np
from helper import *


def process(img, gauss):
    """
    Intensify image around plate-like regions 
    :param img: scaled image
    :param gauss: gaussian image
    """

    # calculate
    mean, sdev = _calculate(img.shape[0], img.shape[1], gauss)

    # apply intensify
    f = np.vectorize(weight)
    ret = f(sdev) * (img - mean) + mean

    # normalize and return
    ret[ret < 0] = 0
    ret[ret > 255] = 255
    return np.uint8(ret)
# end function


def _calculate(row, col, gauss):
    """
    Calculate (mean, and standard deviation) values for Intensifying
    """
    m, n = cfg.BLOCK_COUNT
    h = row // m
    w = col // n

    x, y = np.ogrid[0:1:(1/h), 0:1:(1/w)]
    neg_x = np.float64(1 - x)
    neg_y = np.float64(1 - y)

    mean = np.zeros((row, col), dtype=np.float64)
    sdev = np.zeros((row, col), dtype=np.float64)

    # loop iterators
    win_x, win_y = np.ogrid[0:row:h, 0:col:w]
    win_x = win_x.flatten()
    win_y = win_y.flatten()

    # for all windows
    for i in win_x:
        for j in win_y:
            # local average of four corners
            i_a, d_a = _mean_std(gauss, i, j, h, w)
            i_b, d_b = _mean_std(gauss, i, j + w, h, w)
            i_c, d_c = _mean_std(gauss, i + h, j, h, w)
            i_d, d_d = _mean_std(gauss, i + h, j + w, h, w)

            # calculate local intensity
            upper_l = neg_y * i_a + y * i_b
            lower_l = neg_y * i_c + y * i_d
            mean[i:i + h, j:j + w] = np.dot(neg_x, upper_l) + np.dot(x, lower_l)

            # calculate local standard deviation
            upper_d = neg_y * d_a + y * d_b
            lower_d = neg_y * d_c + y * d_d
            sdev[i:i+h, j:j+w] = np.dot(neg_x, upper_d) + np.dot(x, lower_d)
        # end for j
    # end for i

    return mean, sdev
# end function


def _mean_std(img, i, j, p, q):
    """
    Calculates the mean intensity and standard deviation of a point
    :param img: Original image
    :param i: current row
    :param j: current column
    :param p: window height
    :param q: window width
    """
    row, col = img.shape

    # get window
    x1 = max(0, i - p // 2)
    y1 = max(0, j - q // 2)
    x2 = min(row, i + p // 2)
    y2 = min(col, j + q // 2)
    window = img[x1:x2, y1:y2]

    # calculate mean and std
    mean = np.mean(window)
    std = np.std(window / np.float64(255))
    return mean, std
# end function


def weight(rho):
    """The weighting function

    Parameter:
        rho -- The deviation at current pixel
    """
    a, b = cfg.WEIGHT_DIST
    t = (rho - a) ** 2

    w = 1.0
    if rho < a:
        p = 2 / (a ** 2)
        w = 3.0 / (p * t + 1)
    elif rho < b:
        q = 2 / ((b - a) ** 2)
        w = 3.0 / (q * t + 1)
    else:
        w = 1.0
    # end if

    return w
# end function


def run(prev, cur, scaled):
    """
    Run stage task
    :param prev: Previous stage number
    :param cur: Current stage number
    :param scaled: Stage number for scaled gray image
    """
    runtime = []
    util.log("Stage", cur, "Intensity distribution")
    for read in util.get_images(prev):
        # open image
        gauss = util.stage_image(read, prev)
        gauss = cv2.imread(gauss, cv2.CV_8UC1)

        # scaled image
        gray = util.stage_image(read, scaled)
        gray = cv2.imread(gray, cv2.CV_8UC1)

        # get result
        out, time = util.execute_module(process, gray, gauss)
        runtime.append(time)

        # save to file
        write = util.stage_image(read, cur)
        cv2.imwrite(write, out)

        # log
        util.log("Converted", read, "| %.3f s" % time, stage=cur)
    # end for

    return np.average(runtime)
# end function
