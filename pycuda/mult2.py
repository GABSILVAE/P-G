import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray
import time

import numpy as np

def time_measure(f):
    t0 = time.time()
    f()
    t = time.time()
    return (t - t0)

def mult(X, Y):
    R = np.matrix([[0,0,0],[0,0,0],[0,0,0]])
    R_gpu = gpuarray.to_gpu(R)

    X_gpu = gpuarray.to_gpu(X)
    Y_gpu = gpuarray.to_gpu(Y)

    for r in range (0,renglones):
        for c in range (0,columnas):
            for k in range (0,renglones):
                R_gpu[r,c] += X_gpu[r,k] * Y_gpu[k,c]

    res = (R_gpu).get()
    #print(res)     
    return(res)

A = np.matrix([[1,1,1],[1,1,1],[1,1,1]])
B = np.matrix([[2,2,2],[1,1,1],[2,2,2]])

renglones = A.shape[0]
print("Cantidad de renglones = ",renglones)
columnas = A.shape[1]
print("Cantidad de columnas = ",columnas)

@time_measure
def res():
    mult(A,B)

print(res)