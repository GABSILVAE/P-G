import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img
from openpyxl import Workbook

'''
df = pd.read_csv('Capture_kc1_300cm6.csv')
x = df.astype(int)
plt.imshow(x, cmap = "gray")
plt.show()


y = img.imread('Capture_kc1_150cm2.jpeg')
print(y.shape)
plt.imshow(y, cmap = "gray")
plt.show()

'''
df2 = pd.DataFrame()
df2['Nombre'] = None
df2['Minimo'] = None
df2['Maximo'] = None
df2['Promedio'] = None

name1 = "Capture_kc2_"
dist = 50
cm = "cm"
cont = 1
csv = ".csv"

while(dist < 300):
    if(cont < 7):
        dist = str(dist)
        cont = str(cont)
        name2 = name1 + dist + cm + cont + csv

        df = pd.read_csv(name2)
        image_array = np.array(df)
        a = 0
        y = 0
        max = 0
        min = 255

        for i in range(238,330):
            for j in range(170,270):
                a += 1
                y += image_array[j,i]
                if(image_array[j,i] > max):
                    max = image_array[j,i]
                if(image_array[j,i] < min):
                    min = image_array[j,i]
        prom = y/a 

        nueva_fila = pd.Series([name2,min,max,prom], index=df2.columns)
        df2 = df2.append(nueva_fila, ignore_index=True)
        cont = int(cont) + 1
        dist = int(dist)

    else:
        cont = 1
        dist = int(dist) + 50
        #if(dist == 150 or dist == 250):
        #    dist = int(dist) + 50

df2.to_excel('asd.xlsx', sheet_name='asd')
