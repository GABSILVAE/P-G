import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img

df = pd.read_csv('Capture5.csv')
x = df.astype(int)
plt.imshow(x, cmap = "gray")
plt.show()

'''
y = img.imread('Capture.jpg')
print(y.shape)
plt.imshow(y, cmap = "gray")
plt.show()
'''