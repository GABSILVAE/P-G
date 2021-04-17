from freenect import sync_get_depth as get_depth
import cv2
import numpy as np
from matplotlib import pyplot as plt

kernel = np.ones((5,5),np.float32)/25

def draw():
    depth = get_depth()[0]
    output = depth.astype(np.uint8)
    
    #cv2.imshow('Depth', output)
	dst = cv2.filter2D(output-1,kernel)
	cv2.imshow('Depth', dst)


def loop(function, delay=5):
    while True:
        function()
        cv2.waitKey(delay)
		


loop(draw)

cv2.destroyAllWindows()