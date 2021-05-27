import numpy as np
import pandas as pd
<<<<<<< HEAD
import matplotlib.pyplot as plt
#from StringIO import StringIO

df = pd.read_csv('asd.csv')
x = df.astype(int)

plt.imshow(x, cmap = "gray")
plt.show()
=======
import cv2
import utils
import os

# data
data = pd.read_csv('kinect_valores_50cm_a.csv')  # path of the .csv file
print(data.shape)  # to check the shape
print(data)#print(data.head(5))  # print the first 5 lines of the data
>>>>>>> bd37820744d56488d8cd7fcf39747114e605cd3a
