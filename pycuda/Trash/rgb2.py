import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit




kernel_code_template = """
__global__ void MatrixMulKernel(float *rgbimage, float *grayimage)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
     
    
    if(tx<%(columna)s && ty< %(fila)s){

        int grayOffset = %(columna)s * ty + tx;

        int rgbOffset = grayOffset * %(channels)s;

        unsigned int r = rgbimage[rgbOffset];

        unsigned int g = rgbimage[rgbOffset +1];

        unsigned int b = rgbimage[rgbOffset +2];

        grayimage[grayOffset] = ((r + g + b)/3);
    }
  


}
"""


image=img.imread("shingeki.jpg")


#t= t.astype(np.float32)

fila,columna,canales = image.shape
image_array_list=[]

for row in range(fila):
    for column in range(columna):
        for channel in range (canales):
            image_array_list.append(image[row][column][channel])

image_list=np.array(image_array_list)


image_rgb= np.array(image_list). astype(np.float32)
image_gray=np.zeros((fila,columna)). astype(np.float32)


rgb_gpu = cuda.mem_alloc(image_rgb.nbytes)
gray_gpu = cuda.mem_alloc(image_gray.nbytes)


kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna,
    'channels':canales
    }



mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")

cuda.memcpy_htod(rgb_gpu, image_rgb)


matrixmul(
    # inputs
    rgb_gpu,  
    #output
    gray_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 


gr= np.zeros((fila, columna)). astype(np.float32)


cuda.memcpy_dtoh(gr, gray_gpu)

#gr = gr.astype(np.uint8)


print(image_rgb.shape)
print(image.shape)

figure, axes = plt.subplots(2)


axes[0].imshow(image)
axes[1].imshow(gr)
plt.show()

