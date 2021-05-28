import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

mod = SourceModule("""

     #include <stdio.h>

	__global__ void cuda_dbl(float *dest, float *a){

		const int i = threadIdx.x + blockDim.x * blockIdx.x;
		const int j =  threadIdx.y + blockDim.y * blockIdx.y;
        const int x = j * 5 + i;
        dest[x]= a[x];
	}
""")

a = numpy.ones((5,5))
ans = numpy.zeros_like(a)

func = mod.get_function("cuda_dbl")

func(cuda.Out(ans), cuda.In(a), block=(5,5,1),grid=(1,1,1))

print(ans)