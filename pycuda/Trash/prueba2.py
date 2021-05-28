import numpy as np
from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit


kernel_code_template = """
__global__ void MatrixMulKernel(float *a, float *b, float *c, float *d)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    int i = %(columna)s * ty + tx;
    
    if(tx<%(columna)s && ty< %(fila)s){

          d[i] = a[i]+b[i]+c[i];
    }
  


}
"""


columna=600

fila= 282

a = np.ones((fila,columna))
a = a.astype(np.float32)

print (a)

print ("-" * 80)

b = np.ones((fila,columna))
b = b.astype(np.float32)

c = np.ones((fila,columna))
c = c.astype(np.float32)

print (b)

print ("-" * 80)

print (c)


a_gpu = cuda.mem_alloc(a.nbytes)
b_gpu = cuda.mem_alloc(b.nbytes)
c_gpu = cuda.mem_alloc(c.nbytes)
d_gpu = cuda.mem_alloc(c.nbytes)



kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna
    }
#print(kernel_code)

mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")

cuda.memcpy_htod(a_gpu, a)
cuda.memcpy_htod(b_gpu, b)
cuda.memcpy_htod(c_gpu, c)

matrixmul(
    # inputs
    a_gpu,  
    b_gpu,
    c_gpu,
    #output
    d_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    )  

d= np.zeros_like(a)
cuda.memcpy_dtoh(d, d_gpu)
print ("-" * 80)

print(d)
