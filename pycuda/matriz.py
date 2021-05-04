import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule



mod = SourceModule("""
  __global__ void doublify(float *dest,float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    dest[idx] = 2 * a[idx];
  }
  """)


cuda_dbl = mod.get_function("doublify")

hx=4
hy=4
n= np.array(hx)


A =  2 * np.ones((hx,hy))

print(A)

b,c = A.shape

ans = np.zeros_like(A)

print(ans)

cuda_dbl(drv.Out(ans), drv.In(A), drv.In(n), block = (4,4,1), grid = (1,1,1))


print("####################################")
print(b)
print("####################################")
print(c)
print("####################################")
print(ans)
