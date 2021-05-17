import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit


kernel_code_template = """
__global__ void MatrixMulKernel(float *image, float *kernel, float *imagefiltred)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    float accum=0;

    int kernelRowRadius = %(filfiltro)s/2;
    int kernelColRadius = %(columnfiltro)s/2;

    if(ty < %(fila)s && tx < %(columna)s){

        int startRow= ty - kernelRowRadius;
        int startColumn= tx - kernelColRadius;

        for (int i=0; i<%(filfiltro)s; i++){

            for (int j=0; j< %(columnfiltro)s; j++){

                int currentRow = startRow + i;
                int currentCol = startColumn + j;

                if(currentRow>=0 && currentRow < %(fila)s && currentCol>=0 && currentCol < %(columna)s){

                    accum+= image[(currentRow * %(columna)s + currentCol)] * kernel[i * %(filfiltro)s +j];
                }
                else{

                    accum=0;
                }


            }


        } 
        imagefiltred[ty * %(columna)s + tx] = accum;
    }  

}
"""



image=img.imread("shingeki_gray.jpeg")
canalgrey = image[:,:,0]
print(canalgrey.shape)
'''
filtro=np.array([[-1,0],
                [0,1]])
'''
'''
filtro=np.array([[-1,0],
              [1,0]])
'''

filtro=np.array([[-1,1],
                [0,0]])


print(filtro)
fila,columna=canalgrey.shape
filfiltro,columnfiltro= filtro.shape

image_gray= np.array(canalgrey). astype(np.float32)
filtered=np.array(filtro). astype(np.float32)

img_gpu = cuda.mem_alloc(image_gray.nbytes)
filtro_gpu = cuda.mem_alloc(filtered.nbytes)
filtered_gpu = cuda.mem_alloc(image_gray.nbytes)



kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna,
    'filfiltro':filfiltro,
    'columnfiltro':columnfiltro
    }

print(kernel_code)
print(filtered)



mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


cuda.memcpy_htod(img_gpu, image_gray)
cuda.memcpy_htod(filtro_gpu,filtered)

matrixmul(
    # inputs
    img_gpu,
    filtro_gpu,
    #output
    filtered_gpu, 
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 

gr= np.zeros((fila, columna)). astype(np.float32)


cuda.memcpy_dtoh(gr, filtered_gpu)



figure, axes = plt.subplots(2)
axes[0].imshow(image)
axes[1].imshow(gr,cmap='gray')

plt.show()
