import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

mod = SourceModule("""

     #include <stdio.h>

	__global__ void cuda_dbl(int *dest, int *a){

		const int i = threadIdx.x + blockDim.x * blockIdx.x;
		const int j =  threadIdx.y + blockDim.y * blockIdx.y;
        const int x = j * 25 + i;
        printf(" threadIdx.x:%d.threadIdx.y:%d posglobal:%d\\n", i, j, x);

        dest[x]= 1;
    }

""")

a = numpy.ones((25,25))
b = numpy.zeros((25,25))
func = mod.get_function("cuda_dbl")

func(cuda.Out(b), cuda.In(a),block=(25,25,1),grid=(1,1,1))
print(a)

print("#################################################################")

print(b)













