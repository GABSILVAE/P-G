import numpy as np
from pycuda import driver, compiler, gpuarray, tools

# -- initialize the device
import pycuda.autoinit


kernel_code_template = """
__global__ void MatrixMulKernel(float *a, float *b)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;

    if(ty < %(fila)s && tx < %(columna)s){

        float sum = 0;
        for(int j=0; j< %(n)s;j++){

            sum+=a[j];
        }
        b[0]=sum;
    }

 


}
"""


columna =360

fila= 640

n= fila*columna

a_cpu = np.ones((fila, columna)).astype(np.float32)
b_cpu = np.zeros((columna, fila)).astype(np.float32)


a_gpu = gpuarray.to_gpu(a_cpu) 
b_gpu = gpuarray.to_gpu(b_cpu)



kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna,
    'n': n
    }

mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


matrixmul(
    # inputs
    a_gpu,  
    # output
    b_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (36,16, 1),
    grid = (10,40,1),

    )  

c = b_gpu.get()

print(a_gpu.get())

print ("-" * 80)

print (c[0])