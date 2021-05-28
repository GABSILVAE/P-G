import numpy
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

mod = SourceModule("""

	__global__ void cuda_dbl(float *dest, float *a, float *b, int *n){
		const int i = threadIdx.x + blockDim.x * blockIdx.x;
		if(i<n[0]){ 
			
			dest[i] = a[i] + b[i];
		}
		
	}
""")

cuda_dbl = mod.get_function("cuda_dbl")

a = numpy.ones(5000, dtype = numpy.float32)
b = numpy.ones(4990, dtype = numpy.float32)
n1= 5000
hx=50
n= numpy.array(n1)

ans = numpy.zeros_like(a)

cuda_dbl(drv.Out(ans), drv.In(a), drv.In(b), drv.In(n), block = (hx,1,1), grid = (100,1))

print(n)
print(ans)

