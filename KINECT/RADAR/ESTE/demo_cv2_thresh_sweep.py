#!/usr/bin/env python
"""Sweeps throught the depth image showing 100 range at a time"""
import freenect
import cv2
import numpy as np
import time

from utils2 import green, pol_ncl_5, disp_thresh, objs


lower = 100
upper = 120
max_upper = 256
while upper < max_upper:
    dist = pol_ncl_5((lower + upper) / 2)
    print('%d < depth = %d cm < %d' % (lower, dist, upper))
    img = disp_thresh(lower, upper)
    objs(img)
    #green()
    time.sleep(2)
    lower += 5
    upper += 5