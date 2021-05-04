import pycuda.driver as drv
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pycuda.gpuarray as gpuarray
import numpy
mod = SourceModule("""
__global__ void suma_1_gpu (float *A, float *B)
{
    int i = threadIdx.x + blockDim.x * blockIdx.x;
    if (i < 256){
    
        B[i] = A[i] + 1;
    }
}
""")


suma_1 = mod.get_function("suma_1_gpu")


A_hst = numpy.ones(256, dtype = numpy.float32)
B_hst= numpy.zeros_like(A_hst)

A_gpu = gpuarray.to_gpu(A_hst)
B_gpu= gpuarray.to_gpu(B_hst)

suma_1(A_gpu,B_gpu, block = (256,1,1), grid = (256/256,1))

B_hst= B_gpu.get()


#sum_1(a_gpu, a2_gpu, N, block=(256,1,1), grid=(N/256,1))
#a2_cpu = a2_gpu.get()
print(A_hst)
print (B_hst)