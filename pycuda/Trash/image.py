import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import pandas as pd

image=img.imread("prueba.tiff")
red, row_temp =[],[]
rows,columns,_=image.shape
for row in range (rows):
   for column in range(columns):
      pixel=(float(image[row,column,2]))
      row_temp.append(int(pixel))
   red.append(row_temp)
   row_temp=[]
img=np.array(red)
figure, axes = plt.subplots(2, 3)

a=img.shape
print(a)

b=image.shape
print(a)
'''
suma=0
print(suma)

rows,columns=img.shape
for row in range (rows):
   for column in range (columns):
      suma+=img[row][column]
print(suma)


print(img)
axes[0, 1].imshow(img)
axes[0, 0].imshow(image)
plt.show()
mat=pd.DataFrame(data=img)
mat.to_csv('valores.csv',sep=' ',header=False,float_format='%d',index=False)
'''


