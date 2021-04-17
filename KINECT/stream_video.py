from freenect import sync_get_depth as get_depth
import cv2
import numpy as np


def draw():
    depth = get_depth()[0]
    output = depth.astype(np.uint8)
    
    cv2.imshow('Depth', output)


def loop(function, delay=5):
    while True:
        function()
        cv2.waitKey(delay)


loop(draw)

cv2.destroyAllWindows()