#!/usr/bin/env python
"""Sweeps throught the depth image showing 100 range at a time"""
import freenect
import cv2
import numpy as np
import time

from frame_convert2 import video_cv
from dilatation import dilatation
from erosion import erosion

cv2.namedWindow('Depth')
cv2.namedWindow('puro')
#cv2.namedWindow('video')


def green():
    video, timestamp = freenect.sync_get_video()
    video = video_cv(video)
    video2 = video
    R = video[:,:,0]
    G = video[:,:,1]
    B = video[:,:,2]
    for i in range(641):
        if(i == 213 or i == 214 or i == 427 or i == 428):
            x = i
            R[:,x] = 0
            G[:,x] = 255
            B[:,x] = 0
    R[240,:] = 0
    G[240,:] = 255
    B[240,:] = 0
    video2[:,:,0] = R
    video2[:,:,1] = G
    video2[:,:,2] = B
    cv2.imshow('video', video2)


def pol_ncl_5(val):
    a = 0.0000000153604707187203 * pow(val, 5)
    b = 0.0000102550961463067 * pow(val, 4)
    c = 0.002562964189799 * pow(val, 3)
    d = 0.281730142677474 * pow(val, 2)
    e = 11.860783228931 * val
    y = a - b + c - d + e
    return y


def disp_thresh(lower, upper):
    depth, timestamp = freenect.sync_get_depth()
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = 255 * np.logical_and(depth > lower, depth < upper)
    depth = depth.astype(np.uint8)
    cv2.imshow('Depth', depth)

    filter=np.array([[1,0,1,0,1],
                    [0,1,1,1,0],
                    [1,1,1,1,1],
                    [0,1,1,1,0],
                    [1,0,1,0,1]])
    height_fil, width_fil = filter.shape
    output_dilatation = dilatation(depth, 480, 640, filter, height_fil, width_fil)
    output_dilatation = output_dilatation.astype(np.uint8)
    
    output_erosion = erosion(depth, 480, 640, filter, height_fil, width_fil)
    output_erosion = output_erosion.astype(np.uint8)

    cv2.imshow('puro', output_dilatation)

    cv2.waitKey(10)


lower = 100
upper = 106
max_upper = 256
while upper < max_upper:
    dist = pol_ncl_5((lower + upper) / 2)
    print('%d < depth = %d cm < %d' % (lower, dist, upper))
    disp_thresh(lower, upper)
    #green()
    time.sleep(.1)
    lower += 2
    upper += 2
