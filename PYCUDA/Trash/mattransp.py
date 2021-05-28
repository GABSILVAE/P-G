import numpy as np
from pycuda import driver, compiler, gpuarray, tools

# -- initialize the device
import pycuda.autoinit


kernel_code_template = """
__global__ void MatrixMulKernel(float *a, float *b)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;

    int index = tx + ty * %(columna)s;

    int indtr = ty + tx * %(fila)s;

    b [indtr] = a[index];


}
"""


columna=600

fila= 282

a_cpu = np.random.randn(fila, columna).astype(np.float32)
b_cpu = np.random.randn(columna, fila).astype(np.float32)


a_gpu = gpuarray.to_gpu(a_cpu) 
b_gpu = gpuarray.to_gpu(b_cpu)



kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna
    }

mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


matrixmul(
    # inputs
    a_gpu,  
    # output
    b_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    )  

print(a_gpu.get())

print ("-" * 80)

print (b_gpu.get())