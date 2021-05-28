import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy


mod = SourceModule("""
  __global__ void doublify(float *dest,float *a, int *n)
  {
    int idx = threadIdx.x + threadIdx.y * n[0];

    dest[idx] = 2 * a[idx];
  }
  """)

hx=10
hy=60
n= numpy.array(hx)
a = numpy.ones((hx,hy))

a = a.astype(numpy.float32)

ans = numpy.zeros_like(a)


func = mod.get_function("doublify")
func(cuda.Out(ans), cuda.In(a),cuda.In(n) , block=(hx,hy,1),grid = (1,1,1))




print ("################################################################")
print (a)


print ("################################################################")

print(ans)