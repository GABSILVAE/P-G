import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit




kernel_code_template = """
__global__ void MatrixMulKernel(float *r, float *g, float *b, float *gr)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    int i = %(columna)s * ty + tx;
    
    if(tx<%(columna)s && ty< %(fila)s){

          gr[i] = ((r[i]+g[i]+b[i])/3);
    }
  


}
"""




image=img.imread("shingeki.jpg")

r_img= image[:,:,0]
g_img= image[:,:,1]
b_img= image[:,:,2]

r= r_img.astype(np.float32)
g= g_img.astype(np.float32)
b= b_img.astype(np.float32)

t= np.zeros_like(g_img)
t= t.astype(np.float32)

r_gpu = cuda.mem_alloc(r.nbytes)
b_gpu = cuda.mem_alloc(b.nbytes)
g_gpu = cuda.mem_alloc(g.nbytes)
gr_gpu = cuda.mem_alloc(t.nbytes)

fila,columna,canales = image.shape


kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna
    }


mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")

cuda.memcpy_htod(r_gpu, r)
cuda.memcpy_htod(g_gpu, g)
cuda.memcpy_htod(b_gpu, b)


matrixmul(
    # inputs
    r_gpu,  
    g_gpu,
    b_gpu,
    #output
    gr_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 


gr= np.zeros_like(t)


cuda.memcpy_dtoh(gr, gr_gpu)

gr = gr.astype(np.float32)

c=gr.astype(np.uint8)

print(gr.shape)
print(image.shape)
print(c.shape)
print(np.amin(c))
print(np.amax(c))

figure, axes = plt.subplots(2,2)


axes[0,0].imshow(image)
axes[0,1].imshow(gr)
axes[1,0].imshow(c,cmap='gray')
plt.show()




