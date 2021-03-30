import numpy as np
import cv2
import matplotlib.pyplot as plt
%matplotlib inline

img_raw = cv2.imread('file.png')

type(img_raw)
numpy.ndarray

img_raw.shape
(860,860,3)

plt.imshow(img_raw)

img = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)