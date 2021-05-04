import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

filas =1000
columnas =1000

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
    const int idx = threadIdx.x + blockDim.x * blockIdx.x;
	const int idy =  threadIdx.y + blockDim.y * blockIdx.y;
    const int i = idy * 1000 + idx;
    if(idy<1000 && idx< 1000){

        float sum=0;
        for(int j=0; j<1000 ;j++){

             sum += a[idy * 1000 +j] + b[j* 1000 +idx];
        }

       c[i]=sum;
    }
    
  }
  """)

func = mod.get_function("doublify")
func(a_gpu,b_gpu,n_gpu,c_gpu,block=(thx,thy,1),grid = (40,40,1))

c= numpy.zeros_like(a)
cuda.memcpy_dtoh(c, c_gpu)

print(a)
print ("##############################################################################")
print(b)
print ("##############################################################################")
print(c)