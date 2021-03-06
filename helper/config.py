# -*- coding: utf-8 -*-

# Set True to show log messages
DEBUG = True

##########################################################################

GRAY_RATIO = [0.59, 0.30, 0.11]  # fixed
SCALE_DIM = (480, 640)           # fixed

# edge density
SOBEL_CUTOFF = 75                # keep it low

# gaussian blur
BLUR_SIZE = (60, 60)             # fixed. the kernel size
BLUR_SIGMA = (10.0, 10.0)        # proportional to blur amount
BLUR_CO = 0.004                  # proportional to blur amount

# intensity distribution
BLOCK_COUNT = (8, 8)             # decreasing = decrease quality, increase speed
WEIGHT_DIST = (0.3, 0.5)         # fixed.

# mixture model
MIXTURE_SIZE = (30, 80)          # fixed. mixture kernel size
MIXTURE_SIGMA = 3.2      		 # variance of main lobe towards x axis (keep it low)
MIXTURE_CO = (-0.2, 0.1)         # A < 0, B > 0. (A ~ 2B)
SMOOTH_CUTOFF = 200              # high value removes more noise

##########################################################################

# plate constraints
MIN_HEIGHT = 30     # in pixels
MIN_WIDTH = 75      # in pixels
MIN_AREA = 0.1      # contour_area / image_area
MIN_ASPECT = 0.3    # contour_height / contour_width
MAX_ASPECT = 0.6    # contour_height / contour_width
MAX_ANGLE = 25       # in degrees

PLATE_DIM = (250, 500)

BNW_THRESH = 0      # black and white threshold

##########################################################################


HOR_MINIMUM = 255 * 0.3
HOR_MAXIMUM = 255 * 0.9
CHAR_MIN_HEIGHT = 10

VER_MINIMUM = 255 * 0.3
VER_MAXIMUM = 255 * 0.9
CHAR_MIN_WIDTH = 10