import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray

import numpy as np

def mult(A):
    A_gpu = gpuarray.to_gpu(A)
    #print(A_gpu)

    M = np.matrix([[0,0,0],[0,0,0],[0,0,0]])
    M_gpu = gpuarray.to_gpu(M)
    #print(M_gpu)

    for i in range (0, renglones):
        for j in range (0, columnas):
            M_gpu[i,j] = A_gpu[i,j]*2
    
    res = M_gpu.get()
    return(res)

B = np.matrix([[1,1,1],[1,1,1],[1,1,1]])

renglones = B.shape[0]
#print(renglones)
columnas = B.shape[1]
#print(columnas)

result = mult(B)
print(result)