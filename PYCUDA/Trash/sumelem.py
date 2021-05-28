import numpy
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

mod = SourceModule("""

	__global__ void cuda_dbl(float *dest, float *a , int *n){
		const int i = threadIdx.x + blockDim.x * blockIdx.x;
		if(i<n[0]){ 

            float sum=0.0;
            for(int j=0; j<n[0];j++){

                sum+=a[j];
            }
			
			dest[0] = sum;
		}
		
	}
""")

cuda_dbl = mod.get_function("cuda_dbl")

a = numpy.ones(5000, dtype = numpy.float32)
#b = numpy.ones(4990, dtype = numpy.float32)
n1= 5000
hx=50
n= numpy.array(n1)

ans = numpy.zeros_like(a)

cuda_dbl(drv.Out(ans), drv.In(a), drv.In(n), block = (hx,1,1), grid = (100,1))

print(n)
print(ans[0])
