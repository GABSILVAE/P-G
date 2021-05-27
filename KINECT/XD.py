import numpy as np
import pandas as pd
import cv2
import utils
import os

# data
data = pd.read_csv('kinect_valores_50cm_a.csv')  # path of the .csv file
print(data.shape)  # to check the shape
print(data)#print(data.head(5))  # print the first 5 lines of the data
