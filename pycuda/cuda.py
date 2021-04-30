import numpy
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

mod = SourceModule("""
	__global__ void cuda_dbl(float *dest, float *a){
		const int i = threadIdx.x;
		dest[i] = 2.*a[i];
	}
""")

cuda_dbl = mod.get_function("cuda_dbl")

a = numpy.ones(400, dtype = numpy.float32)
ans = numpy.zeros_like(a)

cuda_dbl(drv.Out(ans), drv.In(a), block = (400,1,1), grid = (1,1))

print(ans)
	
	