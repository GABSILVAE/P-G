import numpy as np
import collections

from image import array2vector_gray

matriz = np.array([ [0,0,0,0,1,0,0,1,1,1],
                    [0,1,1,1,1,0,1,1,1,1],
                    [0,1,0,0,0,1,0,1,1,1],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,1,1,1,0,0],
                    [0,0,0,0,1,1,1,1,1,0],
                    [0,1,0,1,1,1,1,1,1,0],
                    [0,0,0,0,1,1,1,1,1,0],
                    [0,0,0,0,0,1,1,1,1,0],
                    [0,0,0,0,0,0,1,1,1,1]])
islas=2
filas, columnas = matriz.shape
adv = False

for i in range(filas - 2):
    for j in range(columnas - 2):

        if(i == 0 and j == 0 and matriz[i+1,j+1] == 1):
            matriz[i+1,j+1] = islas
        
        if(matriz[i+1,j+1] == 1):
            adv = False
            for m in range(3):
                for n in range(3):
                    if(matriz[i+m,j+n] != 1 and matriz[i+m,j+n] != 0):
                        adv = True
            if(adv):
                matriz[i+1,j+1] = islas
                adv = False
            else:
                islas += 1
                matriz[i+1,j+1] = islas

        if(matriz[i+1,j+1] != 1 and matriz[i+1,j+1] != 0):
            for k in range(3):
                for l in range(3):
                    if(matriz[i+k,j+l] == 1):
                        matriz[i+k,j+l] = matriz[i+1,j+1]

cantidad = array2vector_gray(matriz)
cantidad = collections.Counter(cantidad)

print(matriz)
print(cantidad)
print(islas-1)
print(cantidad[1])
