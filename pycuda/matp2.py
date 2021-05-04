import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

filas =10000
columnas =10000

n= numpy.array(columnas)

a = numpy.ones((filas,columnas))

a = a.astype(numpy.float32)

b = 2 * numpy.ones((filas,columnas))

print(n)

b = b.astype(numpy.float32) 

n_gpu= cuda.mem_alloc(n.nbytes)
a_gpu = cuda.mem_alloc(a.nbytes)
b_gpu = cuda.mem_alloc(b.nbytes)
c_gpu = cuda.mem_alloc(a.nbytes)

cuda.memcpy_htod(a_gpu, a)
cuda.memcpy_htod(b_gpu, b)
cuda.memcpy_htod(n_gpu, n)



thx=25
thy =25

mod = SourceModule("""
  __global__ void doublify(float *a, float *b,float *n,float *c)
  {
    const int i = threadIdx.x + blockDim.x * blockIdx.x;
	const int j =  threadIdx.y + blockDim.y * blockIdx.y;
    const int idx = j * 10000 + i;
    c[idx] = a[idx] + b[idx];
  }
  """)

func = mod.get_function("doublify")
func(a_gpu,b_gpu,n_gpu,c_gpu,block=(thx,thy,1),grid = (400,400,1))



c= numpy.zeros_like(a)

cuda.memcpy_dtoh(c, c_gpu)

#print (a_doubled)
print ("##############################################################################")
print (a)
print ("##############################################################################")
print (c)
print(c[9999][9999])