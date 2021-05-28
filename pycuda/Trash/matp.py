import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy
a = numpy.ones((100,100))

a = a.astype(numpy.float32)

a_gpu = cuda.mem_alloc(a.nbytes)

cuda.memcpy_htod(a_gpu, a)

mod = SourceModule("""
  __global__ void doublify(float *a)
  {
    const int i = threadIdx.x + blockDim.x * blockIdx.x;
	const int j =  threadIdx.y + blockDim.y * blockIdx.y;
     const int idx = j * 100 + i;
    a[idx] *= 2;
  }
  """)

func = mod.get_function("doublify")
func(a_gpu, block=(25,25,1),grid = (4,4,1))

a_doubled = numpy.empty_like(a)
cuda.memcpy_dtoh(a_doubled, a_gpu)

print (a_doubled)
print ("##############################################################################")
print (a)
print ("##############################################################################")

