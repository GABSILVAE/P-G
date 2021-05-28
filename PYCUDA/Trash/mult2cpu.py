import numpy as np
import time

def time_measure(f):
    t0 = time.time()
    f()
    t = time.time()
    return (t - t0)

def mult(X, Y):
    R = np.zeros_like(X)

    for r in range (0,renglones):
        for c in range (0,columnas):
            for k in range (0,renglones):
                R[r,c] += X[r,k] * Y[k,c]

    print(R)     
    return(R)

A = np.ones((100,100))
B = np.ones((100,100))

renglones = A.shape[0]
print("Cantidad de renglones = ",renglones)
columnas = A.shape[1]
print("Cantidad de columnas = ",columnas)

@time_measure
def res():
    mult(A,B)

print(res)