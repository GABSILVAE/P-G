import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from StringIO import StringIO

df = pd.read_csv('asd.csv')
x = df.astype(int)

plt.imshow(x, cmap = "gray")
plt.show()